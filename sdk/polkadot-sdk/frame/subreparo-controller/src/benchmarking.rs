#![cfg(feature = "runtime-benchmarks")]

use super::*;
use frame_benchmarking::{benchmarks, impl_benchmark_test_suite};

benchmarks! {
    on_initialize_observe {
        pallet_subreparo::DriftLevel::<T>::put(T::Tau::get().saturating_add(1));
    }: {
        Pallet::<T>::on_initialize(Default::default());
    }

    on_initialize_apply {
        pallet_subreparo::DriftLevel::<T>::put(T::Tau::get().saturating_add(100));
        ConsecutiveBreaches::<T>::put(T::Persistence::get());
    }: {
        Pallet::<T>::on_initialize(Default::default());
    }
}

impl_benchmark_test_suite!(Pallet, crate::mock::new_test_ext(), crate::mock::Test);
