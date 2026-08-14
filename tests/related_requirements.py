covered_requirement_ids = {
    requirement_id
    for test in tests
    for requirement_id in test.related_requirements
}