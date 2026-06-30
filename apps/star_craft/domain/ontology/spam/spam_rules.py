from star_craft.domain.ontology.spam.spam_taxonomy import SPAM_TAXONOMY, SpamCategory


def classify(subject: str, body: str) -> SpamCategory:
    text = f"{subject} {body}".lower()
    scores: dict[SpamCategory, int] = dict.fromkeys(SpamCategory, 0)

    for category, keywords in SPAM_TAXONOMY.items():
        for keyword in keywords:
            if keyword in text:
                scores[category] += 1

    best = max(scores, key=lambda c: scores[c])
    return best if scores[best] > 0 else SpamCategory.UNKNOWN
