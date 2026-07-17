const API_URL = "http://localhost:5000/api";


// ================= Load Categories =================

function loadCategories() {


    fetch(`${API_URL}/categories`)

        .then(response => response.json())

        .then(data => {


            let table = document.getElementById("categoryTable");


            table.innerHTML = "";


            data.forEach(category => {


                table.innerHTML += `

<tr>

<td>${category.id}</td>


<td>${category.name}</td>


<td>

<button onclick="deleteCategory(${category.id})">
Delete
</button>


</td>


</tr>

`;


            });


        })


        .catch(error => {

            console.log(error);

        });


}



loadCategories();



// ================= Add Category =================


function addCategory() {


    let name = document.getElementById("categoryName").value;



    if (name.trim() == "") {

        alert("Enter Category Name");

        return;

    }



    fetch(`${API_URL}/categories`,
        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },


            body: JSON.stringify({

                name: name

            })


        })


        .then(response => response.json())


        .then(data => {


            alert("Category Added Successfully");


            document.getElementById("categoryName").value = "";


            loadCategories();


        });


}





// ================= Delete Category =================


function deleteCategory(id) {


    let confirmDelete = confirm(
        "Are you sure you want to delete?"
    );



    if (confirmDelete) {


        fetch(`${API_URL}/categories/${id}`,
            {

                method: "DELETE"

            })


            .then(response => response.json())


            .then(data => {


                alert("Category Deleted");


                loadCategories();


            });


    }


}






// ================= Search Category =================


document
    .getElementById("searchCategory")
    .addEventListener("keyup", function () {


        let value = this.value.toLowerCase();


        let rows = document
            .getElementById("categoryTable")
            .getElementsByTagName("tr");



        for (let i = 0; i < rows.length; i++) {


            let text = rows[i]
                .innerText
                .toLowerCase();



            if (text.includes(value)) {

                rows[i].style.display = "";


            }

            else {

                rows[i].style.display = "none";


            }


        }



    });