def compliance_percentage(results):
    if not results:
        return 0.0
    weights = {"Met": 1.0, "Partial": 0.5, "Not Met": 0.0}
    return sum(weights[r.status] for r in results) / len(results) * 100

def domain_breakdown(results, controls_by_id):
    domains = {}
    for r in results:
        domain = controls_by_id[r.control_id].domain
        domains.setdefault(domain, []).append(r)
    return {d: compliance_percentage(rs) for d, rs in domains.items()}
