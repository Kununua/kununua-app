extension StringExtension on String {
    String capitalize() {
      return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
    }

    String capitalizeFirstOfEach() {
      return split(" ").map((str) => str.capitalize()).join(" ");
    }
}