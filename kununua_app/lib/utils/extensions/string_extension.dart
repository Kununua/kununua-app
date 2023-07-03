extension StringExtension on String {
    String capitalize() {
      return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
    }

  String title() {
    return split(" ")
        .map((str) => str.trim().isNotEmpty ? str.capitalize() : '')
        .join(" ");
  }
}