import abc

# TODO:
# 1. code commenting
# 2. error handling
# 3. write tests to test methods


class DataCleanupBase(metaclass=abc.ABCMeta):
    """
    This abstanct class provides methods for data cleanup
    """

    def drop_columns(self, cols):
        self.df.drop(cols, axis=1, inplace=True)

    def remove_nans_rows(self):
        self.df.dropna(inplace=True)

    def remove_duplicate_rows(self):
        self.df.drop_duplicates(inplace=True)

    def change_nans(self, col, new_value):
        self.df[col].fillna(new_value, inplace=True)

    def change_col_values(self, col, regex, new_value):
        self.df[col] = self.df[col].str.replace(regex, new_value, regex=True)

    def col_filter_values(self, col, regex):
        self.df = self.df[self.df[col].astype(str).str.contains(regex, regex=True)]


class DataCleanup(DataCleanupBase):
    """
    This class do data cleanup based on the methhods provided in parent class
    """

    def __init__(self, cleanup_rules):
        self.rules = cleanup_rules

    def cleanup(self, data):
        self.df = data
        self._cleanup()
        return self.df

    def _cleanup(self):
        for rule, func in [
            ("rm-nans", "remove_nans_rows"),
            ("chg-dtypes", "change_data_type"),
            ("rm-dups", "remove_duplicate_rows"),
            ("chg-values", "chg_values"),
            ("filter-values", "filter_values"),
        ]:
            if self.rules.get(rule) and self.rules[rule].get("active"):
                eval(f"self.{func}")()

    def change_data_type(self):
        rules = self.rules["chg-dtypes"]["rules"]
        for chg in rules:
            if chg.get("active"):
                self.df[chg.get("col")] = self.df[chg.get("col")].astype(chg.get("to"))

    def change_values(self):
        rules = self.rules["chg-values"]["rules"]
        [
            self.change_col_values(chg.get("col"), chg.get("from"), chg.get("to"))
            for chg in rules
            if chg.get("active")
        ]

    def filter_values(self):
        rules = self.rules["filter-values"]["rules"]
        [
            self.col_filter_values(chg.get("col"), chg.get("values"))
            for chg in rules
            if chg.get("active")
        ]
