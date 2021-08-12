from itertools import count
from brownie import Wei, reverts
import eth_abi
from brownie.convert import to_bytes
from useful_methods import genericStateOfStrat,genericStateOfVault
import random
import brownie


def test_sbtc_sbtc(Strategy, whale, strategy_sbtc_sbtc, accounts, yvaultv2sbtc, chain, sbtc_vault, ychad, gov, strategist, interface):
    strategist = gov
    vault = sbtc_vault
    currency = interface.ERC20(vault.token())
    decimals = currency.decimals()
    gov = accounts.at(vault.governance(), force=True)
    strategy = strategy_sbtc_sbtc

    yvault = yvaultv2sbtc
    print("curveid: ", strategy.curveId())
    print("curve token: ", strategy.curveToken())
    print("ytoken: ", strategy.yvToken())
    yvault.setDepositLimit(2 **256 -1 , {'from': yvault.governance()})
    currency.approve(vault, 2 ** 256 - 1, {"from": whale})
    whale_before = currency.balanceOf(whale)
    print(currency.name())
    print (whale_before/1e18)
    whale_deposit = 10 * (10 ** (decimals))
    vault.deposit(whale_deposit, {"from": whale})
    vault.setManagementFee(0, {"from": gov})

    vault.addStrategy(strategy, 10_000, 0, 2**256-1, 1000, {"from": gov})

    strategy.harvest({'from': strategist})
    genericStateOfStrat(strategy, currency, vault)
    #genericStateOfStrat(strategy, currency, vault)
    #genericStateOfVault(vault, currency)
    print(yvault.pricePerShare()/1e18)

    ibcrvStrat1 = Strategy.at(yvault.withdrawalQueue(0))
    ibcrvStrat2 = Strategy.at(yvault.withdrawalQueue(1))

    vGov = accounts.at(yvault.governance(), force=True)
    ibcrvStrat1.harvest({"from": vGov})
    ibcrvStrat2.harvest({"from": vGov})
    chain.sleep(2016000)
    chain.mine(1)
    ibcrvStrat1.harvest({"from": vGov})
    ibcrvStrat2.harvest({"from": vGov})
    chain.sleep(21600)
    chain.mine(1)
    print(yvault.pricePerShare()/1e18)
    strategy.harvest({'from': strategist})
    print(vault.strategies(strategy))
    genericStateOfStrat(strategy, currency, vault)
    genericStateOfVault(vault, currency)
    chain.sleep(21600)
    chain.mine(1)

    vault.withdraw(vault.balanceOf(whale),whale, 200,{"from": whale})
    whale_after = currency.balanceOf(whale)
    profit = (whale_after - whale_before)
    print("profit =", profit/(10 ** (decimals)))
    assert profit > 0
    print("balance left =", vault.balanceOf(whale))
    genericStateOfStrat(strategy, currency, vault)
    genericStateOfVault(vault, currency)
    vault.updateStrategyDebtRatio(strategy, 0 , {"from": gov})
    strategy.setDoHealthCheck(False, {"from": gov})

    strategy.harvest({'from': strategist})
    assert vault.strategies(strategy).dict()['totalDebt'] == 0

    genericStateOfStrat(strategy, currency, vault)
