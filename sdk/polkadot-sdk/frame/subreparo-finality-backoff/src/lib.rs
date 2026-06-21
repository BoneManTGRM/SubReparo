#![cfg_attr(not(feature = "std"), no_std)]

pub use pallet::*;
pub mod weights;

#[cfg(test)]
mod mock;

#[cfg(test)]
mod tests;

#[cfg(feature = "runtime-benchmarks")]
mod benchmarking;

#[frame_support::pallet]
pub mod pallet {
    use crate::weights::WeightInfo;
    use frame_support::{pallet_prelude::*, traits::Get};
    use frame_system::pallet_prelude::*;
    use pallet_subreparo as subreparo;

    #[pallet::config]
    pub trait Config: frame_system::Config + subreparo::Config {
        type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;
        type WeightInfo: WeightInfo;

        #[pallet::constant]
        type PauseThreshold: Get<u32>;

        #[pallet::constant]
        type ResumeThreshold: Get<u32>;
    }

    #[pallet::pallet]
    pub struct Pallet<T>(_);

    #[pallet::storage]
    pub type FinalityLag<T> = StorageValue<_, u32, ValueQuery>;

    #[pallet::event]
    #[pallet::generate_deposit(pub(super) fn deposit_event)]
    pub enum Event<T: Config> {
        FinalityLagUpdated(u32),
        BackoffPauseChanged(bool),
    }

    #[pallet::call]
    impl<T: Config> Pallet<T> {
        #[pallet::call_index(0)]
        #[pallet::weight(T::WeightInfo::set_finality_lag())]
        pub fn set_finality_lag(origin: OriginFor<T>, lag: u32) -> DispatchResult {
            T::ControllerOrigin::ensure_origin(origin)?;
            FinalityLag::<T>::put(lag);
            Self::deposit_event(Event::FinalityLagUpdated(lag));
            Self::apply_policy(lag);
            Ok(())
        }
    }

    impl<T: Config> Pallet<T> {
        fn apply_policy(lag: u32) {
            let currently_paused = subreparo::RepairsPaused::<T>::get();
            if lag > T::PauseThreshold::get() && !currently_paused {
                subreparo::RepairsPaused::<T>::put(true);
                Self::deposit_event(Event::BackoffPauseChanged(true));
            } else if lag <= T::ResumeThreshold::get() && currently_paused {
                subreparo::RepairsPaused::<T>::put(false);
                Self::deposit_event(Event::BackoffPauseChanged(false));
            }
        }
    }
}
