use crate::{mock::*, Error, Event};
use frame_support::{assert_noop, assert_ok};

#[test]
fn sample_and_repair_work() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparo::sample_drift(RuntimeOrigin::root(), 120));
        assert_ok!(SubReparo::repair(RuntimeOrigin::root(), 0, 1, 50));
        assert_eq!(pallet_subreparo::DriftLevel::<Test>::get(), 70);
        System::assert_last_event(RuntimeEvent::SubReparo(Event::RepairApplied(50, 70)));
    });
}

#[test]
fn duplicate_nonce_is_rejected() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparo::sample_drift(RuntimeOrigin::root(), 120));
        assert_ok!(SubReparo::repair(RuntimeOrigin::root(), 0, 1, 50));
        pallet_subreparo::EpochCooldownRemaining::<Test>::put(0);
        assert_noop!(
            SubReparo::repair(RuntimeOrigin::root(), 0, 1, 50),
            Error::<Test>::DuplicateNonce
        );
    });
}

#[test]
fn pause_blocks_repair() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparo::sample_drift(RuntimeOrigin::root(), 120));
        assert_ok!(SubReparo::set_paused(RuntimeOrigin::root(), true));
        assert_noop!(
            SubReparo::repair(RuntimeOrigin::root(), 0, 1, 50),
            Error::<Test>::RepairsArePaused
        );
    });
}

#[test]
fn cooldown_blocks_repair() {
    new_test_ext().execute_with(|| {
        assert_ok!(SubReparo::sample_drift(RuntimeOrigin::root(), 120));
        assert_ok!(SubReparo::repair(RuntimeOrigin::root(), 0, 1, 50));
        assert_noop!(
            SubReparo::repair(RuntimeOrigin::root(), 0, 2, 50),
            Error::<Test>::CooldownActive
        );
    });
}
