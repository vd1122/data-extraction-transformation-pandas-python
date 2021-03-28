import abc

# TODO:
# 1. code commenting
# 2. error handling
# 3. write tests


class DataValidationBase(metaclass=abc.ABCMeta):
    """
    This abstanct class provides methods for data validation
    """

    def no_nans(self):
        if self.df.isnull().values.any():
            self._report("fail", "no_nans", "Dataset contains NANs.")
        else:
            self._report("pass", "no_nans", "Dataset does not contain NANs.")

    def no_dups(self):
        if self.df.duplicated().any():
            self._report("fail", "no_dups", "Dataset has duplicates.")
        else:
            self._report(
                "pass", "no_dups", "Dataset does not contain duplicate reecords."
            )

    def col_no_nans(self, col):
        if self.df[col].isnull().values.any():
            self._report("fail", "col_no_nans", f"Column [{col}] has NANs.")
        else:
            self._report("pass", "col_no_nans", "Column [{col}] has no NANs.")

    def col_valid_values(self, col, regex):
        if not all(self.df[col].astype(str).str.contains(regex)):
            self._report(
                "fail",
                "col_valid_values",
                f"Column [{col}] has values not matching {regex}.",
            )
        else:
            self._report(
                "pass",
                "col_valid_values",
                f"Column [{col}] has all values matching {regex}.",
            )

    def _report(self, status, check, message):
        prefix = "OK:" if status == "pass" else "ERROR:"
        self.report[status].append({"check": check, "msg": f"{prefix} {message}"})

    def validation_report(self):
        return self.report


class DataValidation(DataValidationBase):
    """
    This class do data cleanup based on the methhods provided in parent class
    """

    def __init__(self, validation_rules):
        self.rules = validation_rules

    def validate(self, data):
        self.report = {"fail": [], "pass": []}
        self.df = data
        self._validate()

    def _validate(self):
        for rule, func in [
            ("no-dups", "no_dups"),
            ("no-nans", "no_nans"),
            ("cols-no-nans", "cols_no_nans"),
            ("chk-cols-values", "chk_cols_values"),
        ]:
            if self.rules.get(rule) and self.rules[rule].get("active"):
                eval(f"self.{func}")()

    def cols_no_nans(self):
        rules = self.rules["cols-no-nans"]
        [self.col_no_nans(col) for col in rules["cols"]]

    def chk_cols_values(self):
        rules = self.rules["chk-cols-values"]["rules"]
        [
            self.col_valid_values(chk.get("col"), chk.get("values"))
            for chk in rules
            if chk.get("active")
        ]
