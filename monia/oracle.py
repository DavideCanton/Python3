def oracle_max_master(in_neighbors_rules):
    if in_neighbors_rules is not None and len(in_neighbors_rules) != 0:
        rule_max, _ = in_neighbors_rules.most_common(1)[0]
        if rule_max == 1:
            return 1
    return 0


def oracle_max_master_or_journeyer(in_neighbors_rules):
    if in_neighbors_rules is not None and len(in_neighbors_rules) != 0:
        rule_max, _ = in_neighbors_rules.most_common(1)[0]
        if rule_max <= 2:
            return 1
    return 0    
