import random


def dice() -> bool:
    return random.choice([True, False])


def eval_income(gain, bet_amount, bet_raise):
    last_bet_outcome = dice()
    gain += bet_amount if last_bet_outcome else -bet_amount
    bet_amount *= bet_raise
    return last_bet_outcome, gain, bet_amount


def main(min_attempts=100, bet_raise=2, attempts_limit=False):
    gain = 0
    bet_amount = 1

    last_bet_outcome: bool = None
    for _ in range(min_attempts):
        last_bet_outcome, gain, bet_amount = eval_income(
            gain, bet_amount, bet_raise
        )
    current_attempts = min_attempts
    while not last_bet_outcome:
        last_bet_outcome, gain, bet_amount = eval_income(
            gain, bet_amount, bet_raise
        )
        current_attempts += 1
        if current_attempts - min_attempts > 1:
            break

    return last_bet_outcome, gain, bet_amount, current_attempts


if __name__ == '__main__':
    iterations = 100000
    attempt_results = []
    overall_gain = 0
    gains_list = []

    min_attempts = 10
    bet_raise = 2

    stats = {
        'iterations': iterations,
        'min_attempts': min_attempts,
        'bet_raise': bet_raise,
        'max_bet': 0,
        'max_attempt': 0,
        'overall_gain': 0,
    }

    print(
        f'Starting new gambling {iterations} times. '
        f'Multiply bet for {min_attempts} minimum '
        f'attempts plus until successful outcome.\n'
        f'Minimum attepmts: {min_attempts}, bet raise multiplier: {bet_raise}'
    )

    for iteration in range(iterations):
        last_bet_outcome, gain, bet_amount, attempts = main(
            min_attempts=min_attempts,
            bet_raise=bet_raise,
            attempts_limit=True
        )
        positive = gain > 0
        print(f'Won last bet? {last_bet_outcome}')
        print(f'Total gain: {gain}')
        print(f'# your successful bet: {attempts}')
        print(f'Last bet amount: {bet_amount}')
        print(f'Attepmt been successful? {positive}\n')

        attempt_results.append(positive)
        stats['overall_gain'] += gain
        gains_list.append(gain)
        if bet_amount > stats['max_bet']:
            stats['max_bet'] = bet_amount
        if attempts > stats['max_attempt']:
            stats['max_attempt'] = attempts

    gains_list.sort()

    for var, percent in zip(
        ['1', '0.1', '0.01'], [10, 100, 10000]
    ):
        percent_part = int(iterations / percent)
        gains_list_percent = gains_list[percent_part:int(-percent_part)]
        list_percent_gain = sum(gains_list_percent)
        print(f'Gain with cropped {var}%: {list_percent_gain}')

    overall_result = all(attempt_results)

    print(
        f'Have you won every single gamble? {overall_result},\n'
        f'Stats: {stats}'
    )
