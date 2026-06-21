use frame_support::weights::Weight;

pub trait WeightInfo {
    fn on_initialize_observe() -> Weight;
    fn on_initialize_apply() -> Weight;
}

impl WeightInfo for () {
    fn on_initialize_observe() -> Weight {
        Weight::from_parts(10_000, 0)
    }

    fn on_initialize_apply() -> Weight {
        Weight::from_parts(50_000, 0)
    }
}
