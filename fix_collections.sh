#!/bin/bash
set -e
echo "Fixing duplicate collections..."

# 1. Marcus Aurelius -> Meditations
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Marcus Aurelius — Meditations/collection: Meditations/g' {} +
echo "✓ Marcus Aurelius -> Meditations"

# 2. Epictetus Works -> Epictetus, Enchiridion  
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Epictetus Works$/collection: Epictetus, Enchiridion/g' {} +
echo "✓ Epictetus Works -> Epictetus, Enchiridion"

# 3. Kaṭha Upaniṣad -> Katha Upanishad
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Kaṭha Upaniṣad/collection: Katha Upanishad/g' {} +
echo "✓ Kaṭha Upaniṣad -> Katha Upanishad"

# 4. Śvetāśvatara Upaniṣad -> Svetasvatara Upanishad
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Śvetāśvatara Upaniṣad/collection: Svetasvatara Upanishad/g' {} +
echo "✓ Śvetāśvatara Upaniṣad -> Svetasvatara Upanishad"

# 5. Nagarjuna -> Mūlamadhyamakakārikā
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Nagarjuna Mulamadhyamakakarika/collection: Mūlamadhyamakakārikā/g' {} +
echo "✓ Nagarjuna -> Mūlamadhyamakakārikā"

# 6. Songs of Milarepa -> Milarepa Songs
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Songs of Milarepa/collection: Milarepa Songs/g' {} +
echo "✓ Songs of Milarepa -> Milarepa Songs"

# 7. Phaedo -> Phaedo (Plato)
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Phaedo$/collection: Phaedo (Plato)/g' {} +
echo "✓ Phaedo -> Phaedo (Plato)"

# 8. Parmenides Fragments -> Parmenides, On Nature
find data/canonical -name "*.yml" -type f -exec sed -i 's/collection: Parmenides Fragments/collection: Parmenides, On Nature/g' {} +
echo "✓ Parmenides Fragments -> Parmenides, On Nature"

echo "Done!"
