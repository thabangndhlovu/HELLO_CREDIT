def parse_company_profile_schema(schema: dict) -> str:
    MAPPED_RATINGS = ["Aaa", "Aa", "A", "Baa", "Ba", "B", "Caa", "Ca", "C"]

    result = []
    for category, details in schema.items():
        result.append(
            f"\n{category.replace('_', ' ').upper()}:\n  Description: {details['description']}\n  Class Weight: {details['class_weight']}%"
        )
        for metric, metric_desc in details["metric_description"].items():
            result.append(
                f"  Metric: {metric.replace('_', ' ').title()}\n    Description: {metric_desc}\n    Weight: {details['metric_weights'][metric] * 100:.2f}%"
            )

            thresholds = details["metrics"][metric]["thresholds"]
            order = (
                "Increasing"
                if not details["metrics"][metric]["lower_is_better"]
                else "Decreasing"
            )
            thresholds_text = ", ".join([f"{thr[0]} to {thr[1]}" for thr in thresholds])

            # Reverse ratings if order is Increasing (lower_is_better=False)
            ratings = (
                MAPPED_RATINGS[::-1]
                if details["metrics"][metric]["lower_is_better"]
                else MAPPED_RATINGS
            )

            result.append(f"    Rating: {', '.join(ratings)}")
            result.append(f"    Thresholds: {thresholds_text}")
            result.append(f"    Order Preference: {order} order preferred")
    return "\n".join(result)
