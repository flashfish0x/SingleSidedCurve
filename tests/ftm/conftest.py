import pytest
from brownie import config
from brownie import network

@pytest.fixture
def andre(accounts):
    # Andre, giver of tokens, and maker of yield
    yield accounts[0]

@pytest.fixture
def ftm_sms(accounts):
    yield accounts.at("0x72a34AbafAB09b15E7191822A679f28E067C4a16", force=True)
    

@pytest.fixture
def dai(interface):
    #ftm dai!
    yield interface.ERC20('0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E')

@pytest.fixture
def curve_2pool(interface):
    yield interface.ICurveFi('0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40')

@pytest.fixture
def usdc(interface):
    #ftm usdc
    yield interface.ERC20('0x04068DA6C83AFCFA0e13ba15A6696662335D5B75')


@pytest.fixture
def whale(accounts, web3, currency, chain, wbtc, dai, hbtc):
    network.gas_price("0 gwei")
    network.gas_limit(6700000)

    daiAcc = accounts.at("0xb0Fa2BeEe3Cf36a7Ac7E99B885b48538Ab364853", force=True)

    #big binance7 wallet
    #acc = accounts.at('0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8', force=True)
    #big binance8 wallet
    #acc = accounts.at('0x006d0f31a00e1f9c017ab039e9d0ba699433a28c', force=True)
    acc = accounts.at("0xA929022c9107643515F5c777cE9a910F0D1e490C", force=True)
    #big huboi wallet
    hbtcAcc = accounts.at('0x24d48513EAc38449eC7C310A79584F87785f856F', force=True)



    #wbtc account
    wb = accounts.at('0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3', force=True)
    wbtc.transfer(acc, wbtc.balanceOf(wb),  {'from': wb})
    dai.transfer(acc, dai.balanceOf(daiAcc),  {'from': daiAcc})
    dai.transfer(acc, hbtc.balanceOf(hbtcAcc),  {'from': hbtcAcc})



    assert currency.balanceOf(acc)  > 0
    assert wbtc.balanceOf(acc)  > 0
    assert hbtc.balanceOf(acc)  > 0
    yield acc


@pytest.fixture
def dai_vault(pm, gov, rewards, guardian, dai):
    currency = dai
    Vault = pm(config["dependencies"][0]).Vault
    vault = gov.deploy(Vault)
    vault.initialize(currency, gov, rewards, "", "", guardian, {"from": gov})
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    yield vault


@pytest.fixture
def zeroaddress():
    yield "0x0000000000000000000000000000000000000000"

@pytest.fixture
def healthcheck(Contract):
    yield Contract('0xDDCea799fF1699e98EDF118e0629A974Df7DF012')

@pytest.fixture
def usdn3crv(interface):
    yield interface.ICrvV3('0x4f3E8F405CF5aFC05D68142F3783bDfE13811522')
@pytest.fixture
def hCRV(interface):
    yield interface.ICrvV3('0xb19059ebb43466C323583928285a49f558E572Fd')
@pytest.fixture
def curvePool(interface):
    yield interface.ICurveFi('0x4CA9b3063Ec5866A4B82E437059D2C43d1be596F')
@pytest.fixture
def depositUsdn(interface):
    yield interface.ICurveFi('0x094d12e5b541784701FD8d65F11fc0598FBC6332')

@pytest.fixture
def curvePoolObtc(interface):
    yield interface.ICurveFi('0xd5BCf53e2C81e1991570f33Fa881c49EEa570C8D')

@pytest.fixture
def curvePoolTusd(interface):
    yield interface.ICurveFi('0xEcd5e75AFb02eFa118AF914515D6521aaBd189F1')

@pytest.fixture
def curvePoolBbtc(interface):
    yield interface.ICurveFi('0xC45b2EEe6e09cA176Ca3bB5f7eEe7C47bF93c756')

@pytest.fixture
def curvePoolPbtc(interface):
    yield interface.ICurveFi('0x11F419AdAbbFF8d595E7d5b223eee3863Bb3902C')

@pytest.fixture
def ibCurvePool(interface):
    yield interface.ICurveFi('0x2dded6Da1BF5DBdF597C45fcFaa3194e53EcfeAF')

@pytest.fixture
def ib3CRV(interface):
    yield interface.ICrvV3('0x5282a4eF67D9C33135340fB3289cc1711c13638C')


@pytest.fixture
def devms(accounts):
    acc = accounts.at('0x846e211e8ba920B353FB717631C015cf04061Cc9', force=True)
    yield acc

@pytest.fixture
def stratms(accounts):
    acc = accounts.at('0x16388463d60FFE0661Cf7F1f31a7D658aC790ff7', force=True)
    yield acc
@pytest.fixture
def orb(accounts):
    acc = accounts.at('0x710295b5f326c2e47e6dd2e7f6b5b0f7c5ac2f24', force=True)
    yield acc


@pytest.fixture
def ychad(accounts):
    acc = accounts.at('0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52', force=True)
    yield acc

@pytest.fixture
def samdev(accounts):
    #big binance7 wallet
    #acc = accounts.at('0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8', force=True)
    #big binance8 wallet
    acc = accounts.at('0xC3D6880fD95E06C816cB030fAc45b3ffe3651Cb0', force=True)



    yield acc

@pytest.fixture
def token(andre, Token):
    yield andre.deploy(Token)


@pytest.fixture
def gov(accounts):
    # yearn multis... I mean YFI governance. I swear!
    yield accounts[1]


@pytest.fixture
def rewards(gov):
    yield gov  # TODO: Add rewards contract


@pytest.fixture
def guardian(accounts):
    # YFI Whale, probably
    yield accounts[2]

@pytest.fixture
def Vault(pm):
    yield pm(config["dependencies"][0]).Vault


@pytest.fixture
def vault(pm, gov, rewards, guardian, currency):
    Vault = pm(config["dependencies"][0]).Vault
    vault = gov.deploy(Vault)
    vault.initialize(currency, gov, rewards, "", "", guardian)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    yield vault

@pytest.fixture
def dai_vault(pm, gov, rewards, guardian, dai):
    currency = dai
    Vault = pm(config["dependencies"][0]).Vault
    vault = gov.deploy(Vault)
    vault.initialize(currency, gov, rewards, "", "", guardian, {"from": gov})
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    yield vault

@pytest.fixture
def strategist(accounts):
    # You! Our new Strategist!
    yield accounts[3]


@pytest.fixture
def keeper(accounts):
    # This is our trusty bot!
    yield accounts[4]


@pytest.fixture
def strategy_dai_ib(strategist, keeper, live_vault_dai, Strategy, ibCurvePool, ib3CRV, ibyvault,healthcheck):
    strategy = strategist.deploy(Strategy, live_vault_dai, 1_000_000*1e18, 3600, 500, ibCurvePool, ib3CRV, ibyvault,3, True, "ssc ib3crv")
    strategy.setHealthCheck(healthcheck)
    strategy.setKeeper(keeper)
    yield strategy
