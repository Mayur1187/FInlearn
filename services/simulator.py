import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

EVENTS_PATH = Path(__file__).resolve().parent.parent / 'data' / 'events.json'


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _to_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def load_events() -> List[Dict]:
    if not EVENTS_PATH.exists():
        return []
    with EVENTS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def normalize_user_data(user_data: Dict) -> Dict:
    age = _to_int(user_data.get('age'), 22)
    retirement_age = _to_int(user_data.get('retirement_age'), 60)
    annual_income = _to_float(user_data.get('income'), 600000.0)
    starting_savings = _to_float(user_data.get('savings'), 100000.0)

    default_expenses = annual_income * 0.62
    annual_expenses = _to_float(user_data.get('expenses'), default_expenses)
    savings_rate = _to_float(user_data.get('savings_rate'), 0.20)

    profile = str(user_data.get('profile', 'balanced')).strip().lower()
    if profile not in {'conservative', 'balanced', 'aggressive'}:
        profile = 'balanced'

    return {
        'age': _clamp(age, 18, 59),
        'retirement_age': _clamp(retirement_age, age + 1, 70),
        'income': max(annual_income, 100000.0),
        'expenses': max(annual_expenses, 50000.0),
        'savings': max(starting_savings, 0.0),
        'savings_rate': _clamp(savings_rate, 0.05, 0.70),
        'profile': profile,
        'seed': _to_int(user_data.get('seed'), age * 100 + int(annual_income // 10000)),
        'decision_state': user_data.get('decision_state', {}),
    }


def apply_decision(user_data: Dict, decision: str) -> Dict:
    payload = dict(user_data)
    state = dict(payload.get('decision_state') or {})

    if decision == 'invest_more':
        state['extra_invest_rate'] = state.get('extra_invest_rate', 0.0) + 0.015
        state['extra_savings_rate'] = state.get('extra_savings_rate', 0.0) + 0.03
        state['extra_expense_rate'] = state.get('extra_expense_rate', 0.0) - 0.02
    elif decision == 'spend_more':
        state['extra_expense_rate'] = state.get('extra_expense_rate', 0.0) + 0.08
        state['extra_savings_rate'] = state.get('extra_savings_rate', 0.0) - 0.03
    elif decision == 'take_loan':
        state['loan_principal'] = state.get('loan_principal', 0.0) + 500000.0
        state['loan_years'] = max(int(state.get('loan_years', 0)), 8)
        state['loan_interest'] = max(float(state.get('loan_interest', 0.11)), 0.09)
    else:
        return payload

    payload['decision_state'] = state
    return payload


def _ranges_for_profile(profile: str) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    if profile == 'conservative':
        return (0.05, 0.07), (0.05, 0.08)
    if profile == 'aggressive':
        return (0.07, 0.10), (0.09, 0.15)
    return (0.06, 0.09), (0.07, 0.11)


def _loan_payment(principal: float, annual_rate: float, years: int) -> float:
    if principal <= 0 or years <= 0:
        return 0.0
    r = annual_rate
    n = years
    if r <= 0:
        return principal / n
    factor = (1 + r) ** n
    return principal * (r * factor) / (factor - 1)


def simulate_life(user_data: Dict, decisions: List[str] = None) -> Dict:
    data = normalize_user_data(user_data)
    if decisions:
        for d in decisions:
            data = apply_decision(data, d)

    state = data.get('decision_state', {})
    extra_invest = float(state.get('extra_invest_rate', 0.0))
    extra_savings = float(state.get('extra_savings_rate', 0.0))
    extra_expense = float(state.get('extra_expense_rate', 0.0))

    loan_principal = float(state.get('loan_principal', 0.0))
    loan_years = int(state.get('loan_years', 0))
    loan_interest = float(state.get('loan_interest', 0.11))

    salary_range, return_range = _ranges_for_profile(data['profile'])
    rng = random.Random(data['seed'])

    events = load_events()

    age = int(data['age'])
    end_age = int(data['retirement_age'])
    income = float(data['income'])
    expenses = float(data['expenses'])
    net_worth = float(data['savings']) + loan_principal
    savings_rate = _clamp(float(data['savings_rate']) + extra_savings, 0.05, 0.75)

    yearly: List[Dict] = []
    all_event_names: List[str] = []
    fired_events = set()
    loan_payment = _loan_payment(loan_principal, loan_interest, loan_years)

    for current_age in range(age, end_age + 1):
        salary_growth = rng.uniform(*salary_range)
        inflation = rng.uniform(0.04, 0.06)
        invest_growth = rng.uniform(*return_range) + extra_invest

        triggered = []
        one_time_cost = 0.0
        one_time_income = 0.0
        event_expense_spike = 0.0
        event_income_multiplier = 1.0

        for event in events:
            event_name = event.get('name', 'Unknown Event')
            repeatable = bool(event.get('repeatable', False))
            if not repeatable and event_name in fired_events:
                continue

            min_age = int(event.get('min_age', current_age))
            max_age = int(event.get('max_age', current_age))
            if current_age < min_age or current_age > max_age:
                continue

            probability = float(event.get('probability', 0.0))
            force_age = event.get('age')
            should_fire = (force_age is not None and current_age == int(force_age))
            if not should_fire and rng.random() <= probability:
                should_fire = True

            if should_fire:
                fired_events.add(event_name)
                triggered.append(event_name)
                all_event_names.append(event_name)
                one_time_cost += float(event.get('one_time_cost', 0.0))
                one_time_income += float(event.get('one_time_income', 0.0))
                event_expense_spike += float(event.get('expense_spike', 0.0))
                event_income_multiplier *= float(event.get('income_multiplier', 1.0))

        income *= (1.0 + salary_growth) * event_income_multiplier
        expenses *= (1.0 + inflation + extra_expense)
        effective_expenses = expenses + event_expense_spike

        target_savings = income * savings_rate
        actual_savings = max(0.0, min(target_savings, max(income - effective_expenses, 0.0)))

        debt_service = loan_payment if loan_years > 0 and (current_age - age) < loan_years else 0.0
        net_cashflow = actual_savings - one_time_cost + one_time_income - debt_service

        net_worth = max(0.0, (max(net_worth, 0.0) + net_cashflow) * (1.0 + invest_growth))

        yearly.append({
            'age': current_age,
            'income': round(income, 2),
            'expenses': round(effective_expenses + debt_service, 2),
            'savings': round(net_cashflow, 2),
            'net_worth': round(net_worth, 2),
            'salary_growth_pct': round(salary_growth * 100, 2),
            'inflation_pct': round(inflation * 100, 2),
            'investment_growth_pct': round(invest_growth * 100, 2),
            'events': triggered,
        })

    story = generate_financial_story(yearly)
    summary = {
        'start_age': age,
        'end_age': end_age,
        'final_net_worth': round(yearly[-1]['net_worth'] if yearly else net_worth, 2),
        'peak_net_worth': round(max((y['net_worth'] for y in yearly), default=net_worth), 2),
        'events_triggered': sorted(set(all_event_names)),
    }

    return {
        'timeline': yearly,
        'summary': summary,
        'story': story,
        'applied_decision_state': state,
    }


def compare_scenarios(primary_data: Dict, secondary_data: Dict) -> Dict:
    primary = simulate_life(primary_data)
    secondary = simulate_life(secondary_data)

    delta = round(primary['summary']['final_net_worth'] - secondary['summary']['final_net_worth'], 2)
    return {
        'primary': primary,
        'secondary': secondary,
        'comparison': {
            'final_wealth_gap': delta,
            'winner': 'primary' if delta >= 0 else 'secondary',
        },
    }


def generate_financial_story(timeline: List[Dict]) -> str:
    if not timeline:
        return 'No simulation data available yet. Try running your timeline first.'

    final = timeline[-1]
    low_savings_years = [y for y in timeline if y['savings'] < 0]
    event_years = [y for y in timeline if y.get('events')]

    highlights = []
    if event_years:
        first = event_years[0]
        event_names = ', '.join(first['events'])
        highlights.append(f"At age {first['age']}, {event_names} changed your cash flow trajectory.")

    if low_savings_years:
        hardest = low_savings_years[0]
        highlights.append(
            f"Your savings turned negative around age {hardest['age']}, showing a pressure point where expenses outran income."
        )

    growth_phases = [y for y in timeline if y['investment_growth_pct'] >= 10]
    if growth_phases:
        start = growth_phases[0]['age']
        highlights.append(f"Compounding accelerated from age {start}, helping net worth climb faster each year.")

    highlights.append(
        f"By age {final['age']}, your projected net worth reaches Rs {final['net_worth']:,.0f}."
    )

    return ' '.join(highlights)
