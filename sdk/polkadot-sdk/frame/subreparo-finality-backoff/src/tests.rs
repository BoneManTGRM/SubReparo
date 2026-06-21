use crate::mock::*;
use frame_support::assert_ok;

#[test]
fn high_finality_lag_pauses_repairs() {
    new_test_ext().execute_with(|| {
        assert!(!pallet_subreparo::RepairsPaused::<Test>::get());
        assert_ok!(SubReparoFinalityBackoff::set_finality_lag(RuntimeOrigin::root(), 13));
        assert!(pallet_subreparo::RepairsPaused::<Test>::get());
    });
}

#[test]
fn recovered_finality_lag_resumes_repairs() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparoFinalityBackoff::set_finality_lag(RuntimeOrigin::root(), 13));
        assert!(pallet_subreparo::RepairsPaused::<Test>::get());
        assert_ok!(SubReparoFinalityBackoff::set_finality_lag(RuntimeOrigin::root(), 4));
        assert!(!pallet_subreparo::RepairsPaused::<Test>::get());
    });
}
