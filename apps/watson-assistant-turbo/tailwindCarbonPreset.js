const plugin = require("tailwindcss/plugin");
const carbonColors = require("@carbon/colors");
const defaultTheme = require("tailwindcss/defaultTheme");
const carbonVarients = ["g10", "g90", "g100"];

const fontFamily = {
  sans: ["IBM Plex Sans", ...defaultTheme.fontFamily.sans],
  serif: ["IBM Plex Serif", ...defaultTheme.fontFamily.serif],
  mono: ["IBM Plex Mono", ...defaultTheme.fontFamily.mono],
};

const colors = {
  blue: carbonColors.blue,
  red: carbonColors.red,
  gray: carbonColors.gray,
  magenta: carbonColors.magenta,
  purple: carbonColors.purple,
  cyan: carbonColors.cyan,
  teal: carbonColors.teal,
  green: carbonColors.green,
  coolGray: carbonColors.coolGray,
  warmGray: carbonColors.warmGray,
  black: "#000000",
  white: "#ffffff",
  transparent: "transparent",
};

const carbonPlugin = plugin(function ({ addVariant }) {
  addVariant("g10", ".cds--g10 &");
  addVariant("g90", ".cds--g90 &");
  addVariant("g100", ".cds--g100 &");
});

const carbonTheme = {
  fontFamily,
  colors,
};

const carbonPreset = {
  theme: carbonTheme,
  plugins: [carbonPlugin],
  variants: {
    extend: {
      background: carbonVarients,
    },
  },
};

module.exports.carbonPreset = carbonPreset;
