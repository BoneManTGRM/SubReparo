#![cfg_attr(not(feature = "std"), no_std)]

pub use pallet::*;

#[frame_support::pallet]
pub mod pallet {
    use frame_support::{pallet_prelude::*, traits::Get};
    use frame_system::pallet_prelude::*;
    use pallet_subreparo as subreparo;

    #[pallet::config]
    pub trait Config: frame_system::Config + subreparo::Config {
        type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;

        #[pallet::constant]
        type Tau: Get<i64>;

        #[pallet::constant]
        type Gain: Get<i64>;

        #[pallet::constant]
        type MaxStep: Get<i64>;

        #[pallet::constant]
        type Persistence: Get<u32>;
    }

    #[pallet::pallet]
    pub struct Pallet<T>(_);

    #[pallet::storage]
    pub type ConsecutiveBreaches<T> = StorageValue<_, u32, ValueQuery>;

    #[pallet::storage]
    pub type ControllerNonce<T> = StorageValue<_, u64, ValueQuery>;

    #[pallet::event]
    #[pallet::generate_deposit(pub(super) fn deposit_event)]
    pub enum Event<T: Config> {
        ControllerObserved(i64, u32),
        ControllerSuggested(i64),
    }

    #[pallet::hooks]
    impl<T: Config> Hooks<BlockNumberFor<T>> for Pallet<T> {
        fn on_initialize(_n: BlockNumberFor<T>) -> Weight {
            let drift = subreparo::DriftLevel::<T>::get();
            if subreparo::RepairsPaused::<T>::get() {
                ConsecutiveBreaches::<T>::put(0);
                return Weight::zero();
            }

            let tau = T::Tau::get().abs();
            let mut breaches = ConsecutiveBreaches::<T>::get();
            if drift.abs() > tau {
                breaches = breaches.saturating_add(1);
            } else {
                breaches = 0;
            }
            ConsecutiveBreaches::<T>::put(breaches);
            Self::deposit_event(Event::ControllerObserved(drift, breaches));

            if breaches >= T::Persistence::get() && drift != 0 {
                let gain = T::Gain::get().abs().max(1);
                let max_step = T::MaxStep::get().abs();
                let gradient = (drift / gain).clamp(-max_step, max_step);
                let nonce = ControllerNonce::<T>::get().saturating_add(1);
                ControllerNonce::<T>::put(nonce);
                Self::deposit_event(Event::ControllerSuggested(gradient));
                let _ = subreparo::Pallet::<T>::repair(
                    frame_system::RawOrigin::Root.into(),
                    subreparo::EpochIndex::<T>::get(),
                    nonce,
                    gradient,
                );
            }
            Weight::zero()
        }
    }
}
