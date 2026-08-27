FRICTION_COST = {

    "DELAYED_RETRY": 1,

    "IMMEDIATE_RETRY": 1,

    "PAYMENT_LINK": 2,

    "REMINDER": 3,

    "PAYMENT_METHOD_UPDATE": 3,

    "HUMAN_ESCALATION": 8,

    "DO_NOT_CONTACT": 0
}


def calculate_friction(action):

    return FRICTION_COST.get(
        action,
        5
    )


def recovery_efficiency(
    expected_revenue,
    action
):

    friction = calculate_friction(
        action
    )

    return round(
        expected_revenue /
        max(friction, 1),
        2
    )