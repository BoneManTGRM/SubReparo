use frame_support::weights::{constants::RocksDbWeight, Weight};

pub trait WeightInfo {
    fn repair() -> Weight;
    fn set_paused() -> Weight;
    fn sample_drift() -> Weight;
    fn advance_epoch() -> Weight;
}

impl WeightInfo for () {
    fn repair() -> Weight {
        RocksDbWeight::get().reads_writes(6, 5)
    }

    fn set_paused() -> Weight {
        RocksDbWeight::get().writes(1)
    }

    fn sample_drift() -> Weight {
        RocksDbWeight::get().writes(1)
    }

    fn advance_epoch() -> Weight {
        RocksDbWeight::get().reads_writes(1, 1)
    }
}
