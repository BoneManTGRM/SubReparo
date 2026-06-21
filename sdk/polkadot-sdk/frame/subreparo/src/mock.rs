use crate as pallet_subreparo;
use frame_support::{construct_runtime, parameter_types, traits::Everything};
use frame_system as system;
use sp_core::H256;
use sp_runtime::{traits::{BlakeTwo256, IdentityLookup}, BuildStorage};

type Block = frame_system::mocking::MockBlock<Test>;

construct_runtime!(
    pub enum Test
    {
        System: frame_system,
        SubReparo: pallet_subreparo,
    }
);

parameter_types! {
    pub const BlockHashCount: u64 = 250;
    pub const MaxRepairsPerBlock: u32 = 1;
    pub const EpochCooldown: u32 = 2;
    pub const MaxRepairStep: i64 = 100;
}

impl system::Config for Test {
    type BaseCallFilter = Everything;
    type BlockWeights = ();
    type BlockLength = ();
    type DbWeight = ();
    type RuntimeOrigin = RuntimeOrigin;
    type RuntimeCall = RuntimeCall;
    type Nonce = u64;
    type Hash = H256;
    type Hashing = BlakeTwo256;
    type AccountId = u64;
    type Lookup = IdentityLookup<Self::AccountId>;
    type Block = Block;
    type RuntimeEvent = RuntimeEvent;
    type BlockHashCount = BlockHashCount;
    type Version = ();
    type PalletInfo = PalletInfo;
    type AccountData = ();
    type OnNewAccount = ();
    type OnKilledAccount = ();
    type SystemWeightInfo = ();
    type SS58Prefix = ();
    type OnSetCode = ();
    type MaxConsumers = frame_support::traits::ConstU32<16>;
}

impl pallet_subreparo::Config for Test {
    type RuntimeEvent = RuntimeEvent;
    type ControllerOrigin = frame_system::EnsureRoot<u64>;
    type WeightInfo = ();
    type MaxRepairsPerBlock = MaxRepairsPerBlock;
    type EpochCooldown = EpochCooldown;
    type MaxRepairStep = MaxRepairStep;
}

pub fn new_test_ext() -> sp_io::TestExternalities {
    let storage = system::GenesisConfig::<Test>::default().build_storage().unwrap();
    storage.into()
}
