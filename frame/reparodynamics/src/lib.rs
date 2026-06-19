#![cfg_attr(not(feature = "std"), no_std)]

pub use pallet::*;

#[frame_support::pallet]
pub mod pallet {
    use frame_support::{pallet_prelude::*, BoundedVec};
    use frame_system::pallet_prelude::*;

    #[pallet::config]
    pub trait Config: frame_system::Config {
        type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;

        #[pallet::constant]
        type MaxLabelLen: Get<u32>;

        #[pallet::constant]
        type MaxDigestLen: Get<u32>;
    }

    pub type EventId = u64;

    #[derive(Clone, Encode, Decode, Eq, PartialEq, RuntimeDebug, TypeInfo, MaxEncodedLen)]
    pub enum RepairStatus {
        Pending,
        Repaired,
        Verified,
        Rejected,
    }

    #[derive(Clone, Encode, Decode, Eq, PartialEq, RuntimeDebug, TypeInfo, MaxEncodedLen)]
    #[scale_info(skip_type_params(T))]
    pub struct RepairEvent<T: Config> {
        pub id: EventId,
        pub reporter: T::AccountId,
        pub category: BoundedVec<u8, T::MaxLabelLen>,
        pub severity: BoundedVec<u8, T::MaxLabelLen>,
        pub digest: BoundedVec<u8, T::MaxDigestLen>,
        pub status: RepairStatus,
        pub created_at: BlockNumberFor<T>,
    }

    #[pallet::pallet]
    pub struct Pallet<T>(_);

    #[pallet::storage]
    #[pallet::getter(fn next_event_id)]
    pub type NextEventId<T> = StorageValue<_, EventId, ValueQuery>;

    #[pallet::storage]
    #[pallet::getter(fn repair_events)]
    pub type RepairEvents<T: Config> = StorageMap<_, Blake2_128Concat, EventId, RepairEvent<T>>;

    #[pallet::event]
    #[pallet::generate_deposit(pub(super) fn deposit_event)]
    pub enum Event<T: Config> {
        RepairEventSubmitted { event_id: EventId, reporter: T::AccountId },
        RepairStatusUpdated { event_id: EventId, status: RepairStatus },
    }

    #[pallet::error]
    pub enum Error<T> {
        EventNotFound,
        LabelTooLong,
        DigestTooLong,
        EventIdOverflow,
    }

    #[pallet::call]
    impl<T: Config> Pallet<T> {
        #[pallet::call_index(0)]
        #[pallet::weight(10_000)]
        pub fn submit_repair_event(
            origin: OriginFor<T>,
            category: Vec<u8>,
            severity: Vec<u8>,
            digest: Vec<u8>,
        ) -> DispatchResult {
            let reporter = ensure_signed(origin)?;

            let category = BoundedVec::<u8, T::MaxLabelLen>::try_from(category)
                .map_err(|_| Error::<T>::LabelTooLong)?;
            let severity = BoundedVec::<u8, T::MaxLabelLen>::try_from(severity)
                .map_err(|_| Error::<T>::LabelTooLong)?;
            let digest = BoundedVec::<u8, T::MaxDigestLen>::try_from(digest)
                .map_err(|_| Error::<T>::DigestTooLong)?;

            let event_id = NextEventId::<T>::get();
            let next_id = event_id.checked_add(1).ok_or(Error::<T>::EventIdOverflow)?;

            RepairEvents::<T>::insert(event_id, RepairEvent::<T> {
                id: event_id,
                reporter: reporter.clone(),
                category,
                severity,
                digest,
                status: RepairStatus::Pending,
                created_at: frame_system::Pallet::<T>::block_number(),
            });
            NextEventId::<T>::put(next_id);
            Self::deposit_event(Event::RepairEventSubmitted { event_id, reporter });
            Ok(())
        }

        #[pallet::call_index(1)]
        #[pallet::weight(10_000)]
        pub fn update_repair_status(
            origin: OriginFor<T>,
            event_id: EventId,
            status: RepairStatus,
        ) -> DispatchResult {
            let _who = ensure_signed(origin)?;
            RepairEvents::<T>::try_mutate(event_id, |maybe_event| -> DispatchResult {
                let event = maybe_event.as_mut().ok_or(Error::<T>::EventNotFound)?;
                event.status = status.clone();
                Ok(())
            })?;
            Self::deposit_event(Event::RepairStatusUpdated { event_id, status });
            Ok(())
        }
    }
}
