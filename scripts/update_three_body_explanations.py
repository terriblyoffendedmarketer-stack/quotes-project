# update_three_body_explanations.py — Expands the explanations for The Three-Body Problem quotes in quote-bank.json
# Usage: python3 scripts/update_three_body_explanations.py
# Requires: json, pathlib

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QB_PATH = ROOT / "content" / "quote-bank.json"

EXP_1874 = (
    "The battle at Tsinghua University between the April 28 Corps and the Red Faction is not fought with sticks or slogans, but with repurposed anti-aircraft machine guns and military munitions. In the midst of this industrial butchery, Liu zeroes in on the extreme fragility of a fifteen-year-old girl perched on the rooftop waving a battle banner. Notice the startling delicacy of his verbs: the high-caliber round meets almost no resistance in her soft adolescent flesh, whistling away as if passing through empty air, while her body descends slowly, buoyant as a wounded bird clinging to the sky. Liu refuses the standard cinematic language of carnage; instead, he uses lyrical deceleration to suspend her between earth and sky, rendering the madness of factional slaughter through the heartbreaking weightlessness of a child.\n\n"
    "This opening casualty functions as an emblem of collective fever, but its true structural brilliance lies in the emotional trap Liu sets for the reader. When Ye Wenjie is introduced chapters later in the frozen expanse of the Greater Khingan Mountains—felling timber while nursing the raw trauma of her father's public lynching—she recalls her younger sister, Wenxue. Liu repeats the exact visual motif: the slender silhouette dwarfed by an oversized scarlet flag. The anonymous spectacle from the prologue violently collapses into private, irreparable grief. By forcing the reader to first witness the death as anonymous historical collateral and only later reveal it as the protagonist's foundational wound, Liu demonstrates that totalitarian tragedy is never abstract—it is the systematic annihilation of individual lives disguised as glorious collective destiny."
)

EXP_1875 = (
    "The physical horror of the moment is staggering: the young Red Guard has fallen from the roof and landed on the spiked iron pickets of the campus gate, her body impaled while opposing factions continue to use the corpses as target practice. Yet Liu shifts the camera from the macabre mutilation to a singular, horrifying detail—the surviving eye turned toward the summer sky of 1967. There is neither shock nor agony in that unblinking stare, only a petrified, pristine devotion that refuses to die with the brain that housed it. The tension in the sentence lies in this perverse juxtaposition: a child's radiant, romantic fervor perfectly preserved inside the mangled wreckage of modern ideological violence.\n\n"
    "Liu cuts straight to the bone of totalitarian horror by diagnosing what ideology actually steals from the young: not merely their physical lives, but their capacity for disillusionment. Had the girl lived another five seconds to comprehend the bullet, she might have felt fear, pain, or the sudden, shattering betrayal of the cause. Instead, the suddenness of the blast freezes her at the absolute zenith of indoctrination, embalming her in a state of blind ecstasy. By anchoring the date—the blue sky of 1967—Liu grounds this metaphysical tragedy in historical reality. It is a terrifying meditation on how easily youthful innocence can be colonized, transformed into an expendable weapon, and extinguished before it ever has the chance to realize it was betrayed."
)

EXP_1876 = (
    "In the bitter subzero wilderness of the Greater Khingan Mountains, Ye Wenjie works among the Production and Construction Corps felling ancient pines, surrounded by mud, frostbite, and the covert reading of Rachel Carson's Silent Spring. Amidst this bleak labor, a single sensory trigger brings her sister Wenxue back to life: the image of a frail girl dwarfed by a billowing red banner against a violent sky. The contrast is devastating. In the opening chapter, the banner-waver was merely one more faceless zealot consumed by the factional civil war; here, in the quiet solitude of the forest, the memory resurfaces stripped of all revolutionary grandeur, leaving only the sickening knowledge that a sibling died terrified, alone, and unremembered by the machine she served.\n\n"
    "This moment is the vital emotional pivot that prepares Wenjie for Red Coast Base and her eventual decision to invite an extraterrestrial power to cleanse humanity. Western readers often interpret Wenjie's misanthropy as abstract philosophical nihilism, but Liu grounds it in concrete, compounded family bereavement. Her father was beaten to death with leather belts by adolescent girls; her mother betrayed him to save her own skin; and now her younger sister has been ground into dust by the very movement she worshiped. By linking the anonymous rooftop casualty of Chapter 1 directly to Wenjie's private bereavement, Liu closes the circle of her isolation. Wenjie does not betray the human race out of spite; she betrays it because she has watched every shred of tenderness, truth, and familial loyalty devoured by human depravity, leaving nothing worth saving."
)

def update():
    with open(QB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_count = 0
    for q in data:
        if q.get("work") == "The Three-Body Problem" and (q.get("author") in ["Liu Cixin", "Cixin Liu"]):
            quote_text = q.get("quote", "")
            if "fifteen-year-old body" in quote_text:
                q["explanation"] = EXP_1874
                updated_count += 1
                print("Updated quote: fifteen-year-old body")
            elif "single, beautiful eye" in quote_text:
                q["explanation"] = EXP_1875
                updated_count += 1
                print("Updated quote: single, beautiful eye")
            elif "Wenxue" in quote_text:
                q["explanation"] = EXP_1876
                updated_count += 1
                print("Updated quote: Wenxue")

    print(f"Total updated: {updated_count}")
    with open(QB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved content/quote-bank.json successfully.")

if __name__ == "__main__":
    update()
