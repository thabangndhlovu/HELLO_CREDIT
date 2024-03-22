import json
import pytest

# import metrics and test all of them

metrics = {
    "profitability": {
        "class_weight": 0.35,
        "weights": [1.0],
        "metrics": {
            "oper_margin": {
                "lower_is_better": False,
                "thresholds": [
                    (0.4, float("inf")),
                    (0.35, 0.4),
                    (0.3, 0.35),
                    (0.25, 0.3),
                    (0.2, 0.25),
                    (0.15, 0.2),
                    (0.1, 0.15),
                    (0.05, 0.1),
                    (0.0, 0.05),
                ],
            }
        },
    },
    "leverage_coverage": {
        "class_weight": 0.65,
        "weights": [0.4, 0.3, 0.3],
        "metrics": {
            "debt_to_equity": {
                "lower_is_better": True,
                "thresholds": [
                    (0, 0.4),
                    (0.4, 0.8),
                    (0.8, 1.2),
                    (1.2, 1.6),
                    (1.6, 2),
                    (2, 2.5),
                    (2.5, 3),
                    (3, 4),
                    (4, float("inf")),
                ],
            },
            "tot_debt_to_ebitda": {
                "lower_is_better": True,
                "thresholds": [
                    (0, 0.4),
                    (0.4, 0.8),
                    (0.8, 1.2),
                    (1.2, 1.6),
                    (1.6, 2),
                    (2, 2.5),
                    (2.5, 3),
                    (3, 4),
                    (4, float("inf")),
                ],
            },
            "ebitda_to_tot_int_exp": {
                "lower_is_better": False,
                "thresholds": [
                    (25, float("inf")),
                    (20, 25),
                    (15, 20),
                    (10, 15),
                    (5, 10),
                    (3, 5),
                    (1, 3),
                    (0, 1),
                    (-float("inf"), 0),
                ],
            },
        },
    },
}


def test_metrics_structure():
    assert isinstance(metrics, dict), "Metrics should be a dictionary"
    assert sum([metrics[clas]['class_weight'] for clas in metrics]) == 1.0, "Sum of class_weights must sum to 1.0"

    for category, data in metrics.items():
        
        # Check if key structures are correct
        assert 'class_weight' in data, f"{category} missing 'class_weight'"
        assert 'weights' in data, f"{category} missing 'weights'"
        assert 'metrics' in data, f"{category} missing 'metrics'"

        # Check types
        assert isinstance(data['class_weight'], float), f"{category} 'class_weight' should be float"
        assert isinstance(data['weights'], list), f"{category} 'weights' should be list"
        assert isinstance(data['metrics'], dict), f"{category} 'metrics' should be dict"
        
        # Check values
        assert data['class_weight'] < 1.0, f"{category} 'class_weight' must be less than 1.0"
        assert sum(data['weights']) == 1.0, f"{category} 'weights' must sum to 1.0"

        for metric, metric_data in data['metrics'].items():
            assert 'lower_is_better' in metric_data, f"{metric} missing 'lower_is_better'"
            assert 'thresholds' in metric_data, f"{metric} missing 'thresholds'"

            # Check types
            assert isinstance(metric_data['lower_is_better'], bool), f"{metric} 'lower_is_better' should be bool"
            assert isinstance(metric_data['thresholds'], list), f"{metric} 'thresholds' should be list"
            assert len(metric_data['thresholds']) == 9, f"{metric} 'thresholds' len should be 9"

            # Check thresholds structure
            for threshold in metric_data['thresholds']:
                assert len(threshold) == 2, f"{metric} threshold should have two elements (lower, higher)"
                assert all(isinstance(n, (float, int)) or n is float('inf') for n in threshold), f"{metric} threshold elements should be numeric or infinity"

