ret_val = list()

ret_val.append("""

Hans Siemens
born: 1818
death: 1867
birth place id: None
place lived id: None


Julie Wiggen
born: 1965-05-23
death: None
birth place id: m.05b4w
place lived id: None

NO, they could not have met by fetched time
NO, I have no information about one or both persons birthplace
NO, I have no information about one or both persons place they lived
""")

ret_val.append("""



Julie Wiggen
born: 1965-05-23
death: None
birth place id: m.05b4w
place lived id: None
nonexisting not found. Exiting program.
""")

ret_val.append("""

Dietrich Rusche
born: 1936-09-13
death: None
birth place id: m.0156q
place lived id: None


Margit Schaumäker
born: 1925-05-12
death: None
birth place id: m.0156q
place lived id: None

YES, they could have met by fetched time
YES, they have the same birthplace
NO, I have no information about one or both persons place they lived
""")
