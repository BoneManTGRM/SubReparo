#![cfg(feature = "runtime-benchmarks")]

use super::*;
use frame_benchmarking::{benchmarks, impl_benchmark_test_suite};
use frame_system::RawOrigin;

benchmarks! {
    sample_drift {
    }: _(RawOrigin::Root, 100_i64)

    repair {
        DriftLevel::<T>::put(100_i64);
    }: _(RawOrigin::Root, 0_u32, 1_u64, 25_i64)

    set_paused {
    }: _(RawOrigin::Root, true)

    advance_epoch {
    }: _(RawOrigin::Root)
}

impl_benchmark_test_suite!(Pallet, crate::mock::new_test_ext(), crate::mock::Test);
