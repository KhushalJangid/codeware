const select = document.getElementById("filechooser");

select.addEventListener("change", (event) => {
    if (event.target.value === "py") {
      editor.setValue(lang_dic["python"]);
    } else if (event.target.value === "js") {
      editor.setValue(lang_dic["javascript"]);
    } else if (event.target.value === "c") {
      editor.setValue(lang_dic["c"]);
    } else if (event.target.value === "cpp") {
      editor.setValue(lang_dic["c++"]);
    } else if (event.target.value === "dart") {
      editor.setValue(lang_dic["dart"]);
    } else if (event.target.value === "java") {
      editor.setValue(lang_dic["java"]);
    }
  });

  let lang_dic = {
    python: `print("hello world")`,
    "c++": `#include <iostream>
using namespace std;

int main() {
  cout << "Hello World!";
  return 0;
}`,
    c: `#include <stdio.h>

int main() {
  printf("Hello World!");
  return 0;
}`,
java:`public class Main {
  public static void main(String[] args) {
      System.out.println("Hello, World!"); 
  }
}`,
    javascript: `console.log("hello wold");`,
    dart: `void main(){
  print("Hello World");
}`,
  };
