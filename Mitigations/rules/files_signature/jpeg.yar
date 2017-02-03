rule jpeg
{
    strings:
        $jpeg1_1 = {FF D8 FF E0 ?? ?? 4A 46 49 46 00}
        $jpeg2_1 = {FF D8 FF E1 ?? ?? 45 78}
        $jpeg2_2 = {69 66 00}
        $jpeg3_1 = {FF D8 FF E8 ?? ?? 53 50}
        $jpeg3_2 = {49 46 46 00}

    condition:
        $jpeg1_1 or ($jpeg2_1 and $jpeg2_2) or ($jpeg3_1 and $jpeg3_2)
}