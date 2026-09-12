from backend.adaptive.service import global_difficulty, mastery_band


def test_mastery_band_boundaries() -> None:
    assert mastery_band(0) == ("BEGINNER", 20.0)
    assert mastery_band(29.99) == ("BEGINNER", 20.0)
    assert mastery_band(30) == ("DEVELOPING", 40.0)
    assert mastery_band(50) == ("INTERMEDIATE", 60.0)
    assert mastery_band(70) == ("PROFICIENT", 80.0)
    assert mastery_band(90) == ("MASTERED", 95.0)
    assert mastery_band(100) == ("MASTERED", 95.0)


def test_global_difficulty_uses_blueprint_weights() -> None:
    # 60% incorrect rate + neutral 25% timing + full 15% reliability.
    assert global_difficulty(0.5, 10) == 57.5
    assert global_difficulty(0, 0) == 12.5
    assert global_difficulty(1, 100) == 87.5
