function addField(plusElement) {

    let displayButton = document.querySelector("#button_box");

    // Create div container
    let div = document.createElement("div");
    div.setAttribute("class", "pdf_file_store");

    let id_value = `pdf-${counter}`

    // Create input field
    let field = document.createElement("input");
    field.setAttribute("type", "file");
    field.setAttribute("id", id_value);
    field.setAttribute("name", id_value);
    field.setAttribute("accept", ".pdf");

    // Create +
    let plus = document.createElement("span");
    plus.setAttribute("onclick", "addField(this)");

    let plusText = document.createTextNode("+");
    plus.appendChild(plusText);

    // Create -
    let minus = document.createElement("span");
    minus.setAttribute("onclick", "removeField(this)");

    let minusText = document.createTextNode("-");
    minus.appendChild(minusText);

    // Add elements to the DOM
    form.insertBefore(div, displayButton);
    div.appendChild(field);
    //div.appendChild(plus);
    //div.appendChild(minus);

    counter++;

    // Show the minus sign && hide the plus sign
    //plusElement.nextElementSibling.style.display = "block";
    //plusElement.style.display = "none";
}

/////

function removeField(minusElement) {
    minusElement.parentElement.remove();
}

/////

let form = document.forms[0];
let counter = 1;