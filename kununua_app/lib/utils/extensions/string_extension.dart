extension StringExtension on String {
    String capitalize() {
      return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
    }

    String capitalizeFirstOfEach() {
      return split(" ").map((str) => str.capitalize()).join(" ");
    }

    String limitCharacters(int limit) {
      int letterCount = 0;
      String newTitle = "";

      for (String word in split(" ")){
        
        if(word.trim() == "") continue;

        letterCount += word.length;
        if (letterCount > limit){
          newTitle = "${newTitle.trim()}…";
          break;
        }else{
          newTitle += "$word ";
        }
      }
      
      return newTitle.trim();
    }
}