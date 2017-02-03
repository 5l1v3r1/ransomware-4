rule png
{
    strings:
        $png = {89 50 4E 47 0D 0A 1A 0A}

    condition:
        all of them
}