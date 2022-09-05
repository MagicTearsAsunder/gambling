import random


def dice(win_rate) -> bool:
    return random.random() < win_rate


def eval_income(gain, bet_amount, win_rate, coefficient, goal_gain):
    last_bet_outcome = dice(win_rate)
    gain += (bet_amount * (coefficient - 1)) if last_bet_outcome else -bet_amount
    if not last_bet_outcome:
        bet_amount = eval_new_bet(gain, goal_gain, coefficient)
    return last_bet_outcome, gain, bet_amount


def eval_new_bet(gain, goal_gain, coefficient):
    return int((abs(gain) + goal_gain) / (coefficient - 1) + 1)


def main(win_rate, coefficient, goal_gain):
    gain = 0
    bet_amount = eval_new_bet(gain, goal_gain, coefficient)

    last_bet_outcome: bool = None

    current_attempts = 0
    while not last_bet_outcome:
        last_bet_outcome = dice(win_rate)
        gain += (bet_amount * coefficient) - bet_amount if last_bet_outcome else -bet_amount

        if not last_bet_outcome:
            bet_amount = eval_new_bet(gain, goal_gain, coefficient)

        current_attempts += 1

    return last_bet_outcome, gain, bet_amount, current_attempts


if __name__ == '__main__':
    win_rate = 0.2
    coefficient = 1.2
    goal_gain = 100

    assert coefficient > 1, "Coefficient can't be less than 1"

    iterations = 10000
    attempt_results = []
    overall_gain = 0
    gains_list = []

    stats = {
        'iterations': iterations,
        'max_bet': 0,
        'max_attempt': 0,
        'overall_gain': 0,
    }

    for _ in range(iterations):
        last_bet_outcome, gain, bet_amount, attempts = main(
            win_rate, coefficient, goal_gain
        )
        positive = gain >= 0
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
