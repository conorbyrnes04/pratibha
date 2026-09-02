export type FilterSelectOption = {
  value: string;
  label: string;
  hint?: string;
  icon?: string;
};

export type FilterSelectProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: FilterSelectOption[];
  /** Gold for collections, lapis for themes */
  tone?: "gold" | "lapis";
  placeholder?: string;
};
