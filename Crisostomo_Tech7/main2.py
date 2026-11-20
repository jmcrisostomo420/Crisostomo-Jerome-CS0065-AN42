data = [2, 4, 10, 12, 3, 20, 30, 11, 25]
centroids = [4, 11]  # Initial M1 and M2

for iteration in range(1, 4):
    clusters = [[], []]

    print(f"\nIteration {iteration}")
    print(f"Centroids: M1={centroids[0]}, M2={centroids[1]}")

    for point in data:
        d1 = abs(point - centroids[0])
        d2 = abs(point - centroids[1])

        # Assign the point to the nearest centroid.
        cluster_index = 0 if d1 <= d2 else 1
        clusters[cluster_index].append(point)

        cluster_name = f"C{cluster_index + 1}"
        print(f"{point:>2}: D1={d1:>5}, D2={d2:>5} -> {cluster_name}")

    # Update each centroid to its cluster's mean.
    centroids = [
        sum(cluster) / len(cluster) if cluster else centroids[i]
        for i, cluster in enumerate(clusters)
    ]

    print(f"C1 = {clusters[0]}")
    print(f"C2 = {clusters[1]}")
    print(f"Updated centroids: M1={centroids[0]}, M2={centroids[1]}")