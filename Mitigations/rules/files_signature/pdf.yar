rule pdf
{
    strings:
        $pdf = {25 50 44 46}

    condition:
        all of them
}