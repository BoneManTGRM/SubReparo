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

    #[pallet::config]
    pub trait Config: frame_system::Config {
        type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;
        type ControllerOrigin: EnsureOrigin<Self::RuntimeOrigin>;
        type WeightInfo: WeightInfo;

        #[pallet::constant]
        type MaxRepairsPerBlock: Get<u32>;

        #[pallet::constant]
        type EpochCooldown: Get<u32>;

        #[pallet::constant]
        type MaxRepairStep: Get<i64>;
    }

    #[pallet::pallet]
    pub struct Pallet<T>(_);

    #[pallet::storage]
    pub type DriftLevel<T> = StorageValue<_, i64, ValueQuery>;

    #[pallet::storage]
    pub type EpochIndex<T> = StorageValue<_, u32, ValueQuery>;

    #[pallet::storage]
    pub type SeenNonces<T> = StorageMap<_, Blake2_128Concat, (u32, u64), (), OptionQuery>;

    #[pallet::storage]
    pub type RepairsPaused<T> = StorageValue<_, bool, ValueQuery>;

    #[pallet::storage]
    pub type RepairsThisBlock<T> = StorageValue<_, u32, ValueQuery>;

    #[pallet::storage]
    pub type EpochCooldownRemaining<T> = StorageValue<_, u32, ValueQuery>;

    #[pallet::event]
    #[pallet::generate_deposit(pub(super) fn deposit_event)]
    pub enum Event<T: Config> {
        DriftSampled(i64),
        RepairApplied(i64, i64),
        RepairsPaused(bool),
        EpochAdvanced(u32),
    }

    #[pallet::error]
    pub enum Error<T> {
        NoDriftDetected,
        RepairBudgetExceeded,
        CooldownActive,
        RepairsArePaused,
        DuplicateNonce,
        BadEpoch,
        ZeroGradient,
    }

    #[pallet::call]
    impl<T: Config> Pallet<T> {
        #[pallet::call_index(0)]
        #[pallet::weight(T::WeightInfo::repair())]
        pub fn repair(origin: OriginFor<T>, epoch: u32, nonce: u64, gradient: i64) -> DispatchResult {
            T::ControllerOrigin::ensure_origin(origin)?;
            ensure!(!RepairsPaused::<T>::get(), Error::<T>::RepairsArePaused);
            ensure!(EpochIndex::<T>::get() == epoch, Error::<T>::BadEpoch);
            ensure!(EpochCooldownRemaining::<T>::get() == 0, Error::<T>::CooldownActive);
            ensure!(SeenNonces::<T>::get((epoch, nonce)).is_none(), Error::<T>::DuplicateNonce);
            ensure!(gradient != 0, Error::<T>::ZeroGradient);

            let count = RepairsThisBlock::<T>::get();
            ensure!(count < T::MaxRepairsPerBlock::get(), Error::<T>::RepairBudgetExceeded);

            let mut drift = DriftLevel::<T>::get();
            ensure!(drift != 0, Error::<T>::NoDriftDetected);

            let max_step = T::MaxRepairStep::get().abs();
            let bounded_gradient = gradient.clamp(-max_step, max_step);
            let correction = bounded_gradient.clamp(-drift.abs(), drift.abs());
            drift = drift.saturating_sub(correction);

            DriftLevel::<T>::put(drift);
            RepairsThisBlock::<T>::put(count.saturating_add(1));
            EpochCooldownRemaining::<T>::put(T::EpochCooldown::get());
            SeenNonces::<T>::insert((epoch, nonce), ());
            Self::deposit_event(Event::RepairApplied(correction, drift));
            Ok(())
        }

        #[pallet::call_index(1)]
        #[pallet::weight(T::WeightInfo::set_paused())]
        pub fn set_paused(origin: OriginFor<T>, paused: bool) -> DispatchResult {
            T::ControllerOrigin::ensure_origin(origin)?;
            RepairsPaused::<T>::put(paused);
            Self::deposit_event(Event::RepairsPaused(paused));
            Ok(())
        }

        #[pallet::call_index(2)]
        #[pallet::weight(T::WeightInfo::sample_drift())]
        pub fn sample_drift(origin: OriginFor<T>, drift: i64) -> DispatchResult {
            T::ControllerOrigin::ensure_origin(origin)?;
            DriftLevel::<T>::put(drift);
            Self::deposit_event(Event::DriftSampled(drift));
            Ok(())
        }

        #[pallet::call_index(3)]
        #[pallet::weight(T::WeightInfo::advance_epoch())]
        pub fn advance_epoch(origin: OriginFor<T>) -> DispatchResult {
            T::ControllerOrigin::ensure_origin(origin)?;
            let next = EpochIndex::<T>::get().saturating_add(1);
            EpochIndex::<T>::put(next);
            Self::deposit_event(Event::EpochAdvanced(next));
            Ok(())
        }
    }

    #[pallet::hooks]
    impl<T: Config> Hooks<BlockNumberFor<T>> for Pallet<T> {
        fn on_initialize(_n: BlockNumberFor<T>) -> Weight {
            RepairsThisBlock::<T>::put(0);
            let rem = EpochCooldownRemaining::<T>::get();
            if rem > 0 {
                EpochCooldownRemaining::<T>::put(rem.saturating_sub(1));
            }
            Weight::zero()
        }
    }
}
