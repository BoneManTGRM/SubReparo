use crate::mock::*;
use frame_support::assert_ok;

#[test]
fn controller_repairs_after_persistence() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparo::sample_drift(RuntimeOrigin::root(), 120));
        SubReparoController::on_initialize(1);
        assert_eq!(pallet_subreparo::DriftLevel::<Test>::get(), 120);
        SubReparoController::on_initialize(2);
        assert!(pallet_subreparo::DriftLevel::<Test>::get() < 120);
    });
}

#[test]
fn controller_resets_breaches_below_tau() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparo::sample_drift(RuntimeOrigin::root(), 10));
        SubReparoController::on_initialize(1);
        assert_eq!(pallet_subreparo_controller::ConsecutiveBreaches::<Test>::get(), 0);
    });
}
