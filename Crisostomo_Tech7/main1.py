from math import log2

# Each row stores the number of planets with these feature values.
data = [
    {"Size": "Big",   "Orbit": "Near", "Habitable": "Yes", "Count": 20},
    {"Size": "Big",   "Orbit": "Far",  "Habitable": "Yes", "Count": 170},
    {"Size": "Small", "Orbit": "Near", "Habitable": "Yes", "Count": 139},
    {"Size": "Small", "Orbit": "Far",  "Habitable": "Yes", "Count": 45},
    {"Size": "Big",   "Orbit": "Near", "Habitable": "No",  "Count": 130},
    {"Size": "Big",   "Orbit": "Far",  "Habitable": "No",  "Count": 30},
    {"Size": "Small", "Orbit": "Near", "Habitable": "No",  "Count": 11},
    {"Size": "Small", "Orbit": "Far",  "Habitable": "No",  "Count": 255},
]

def class_counts(rows):
    return {
        label: sum(row["Count"] for row in rows if row["Habitable"] == label)
        for label in ("Yes", "No")
    }

def entropy(counts):
    total = sum(counts.values())
    if total == 0:
        return 0

    return -sum(
        (count / total) * log2(count / total)
        for count in counts.values()
        if count > 0
    )

def information_gain(rows, feature):
    parent_entropy = entropy(class_counts(rows))
    total = sum(row["Count"] for row in rows)
    weighted_child_entropy = 0

    for value in {row[feature] for row in rows}:
        subset = [row for row in rows if row[feature] == value]
        subset_total = sum(row["Count"] for row in subset)
        weighted_child_entropy += (
            subset_total / total * entropy(class_counts(subset))
        )

    return parent_entropy - weighted_child_entropy

def id3(rows, features):
    counts = class_counts(rows)

    # Stop if this node contains only one class, or there are no features left.
    if counts["Yes"] == 0 or counts["No"] == 0 or not features:
        prediction = "Yes" if counts["Yes"] >= counts["No"] else "No"
        return {"counts": counts, "prediction": prediction}

    best_feature = max(features, key=lambda f: information_gain(rows, f))
    remaining_features = [f for f in features if f != best_feature]

    branches = {}
    for value in {row[best_feature] for row in rows}:
        subset = [row for row in rows if row[best_feature] == value]
        branches[value] = id3(subset, remaining_features)

    return {
        "feature": best_feature,
        "counts": counts,
        "branches": branches,
    }

def print_tree(node, indent=""):
    counts = node["counts"]

    if "feature" not in node:
        print(
            f"{indent}Leaf: predict {node['prediction']} "
            f"(Yes={counts['Yes']}, No={counts['No']})"
        )
        return

    print(
        f"{indent}{node['feature']} "
        f"(Yes={counts['Yes']}, No={counts['No']})"
    )
    for value, child in sorted(node["branches"].items()):
        print(f"{indent}  {value}:")
        print_tree(child, indent + "    ")

def predict(tree, sample):
    node = tree
    while "feature" in node:
        node = node["branches"][sample[node["feature"]]]
    return node["prediction"]

tree = id3(data, ["Size", "Orbit"])

print("Root information gains:")
for feature in ["Size", "Orbit"]:
    print(f"  {feature}: {information_gain(data, feature):.3f}")

print("\nDecision tree:")
print_tree(tree)

print("\nPredictions:")
print("Big, Far:", predict(tree, {"Size": "Big", "Orbit": "Far"}))
print("Small, Near:", predict(tree, {"Size": "Small", "Orbit": "Near"}))