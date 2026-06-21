use frame_support::weights::{constants::RocksDbWeight, Weight};

pub trait WeightInfo {
    fn set_finality_lag() -> Weight;
}

impl WeightInfo for () {
    fn set_finality_lag() -> Weight {
        RocksDbWeight::get().reads_writes(1, 2)
    }
}
