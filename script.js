// ==========================================
// CHANDU TECHNOLOGIES
// SMART INVOICE GENERATOR
// ==========================================


let products = [];

let selectedProductIndex = -1;

let editingProductIndex = -1;


// ==========================================
// INITIAL LOAD
// ==========================================

window.onload = function () {

    updateInvoiceDetails();

    calculateTotals();

};


// ==========================================
// INVOICE NUMBER + DATE
// ==========================================

function updateInvoiceDetails() {

    const now = new Date();

    const year = now.getFullYear();

    const month = String(
        now.getMonth() + 1
    ).padStart(2, "0");

    const day = String(
        now.getDate()
    ).padStart(2, "0");

    const hours = String(
        now.getHours()
    ).padStart(2, "0");

    const minutes = String(
        now.getMinutes()
    ).padStart(2, "0");

    const seconds = String(
        now.getSeconds()
    ).padStart(2, "0");


    const invoiceNumber =
        `INV-${year}${month}${day}-${hours}${minutes}${seconds}`;


    document.getElementById(
        "invoiceNumber"
    ).textContent = invoiceNumber;


    document.getElementById(
        "invoiceDate"
    ).textContent =
        `${day}-${month}-${year}`;
}


// ==========================================
// ADD PRODUCT
// ==========================================

function addProduct() {

    const productName =
        document.getElementById(
            "productName"
        ).value.trim();


    const quantity =
        Number(
            document.getElementById(
                "quantity"
            ).value
        );


    const price =
        Number(
            document.getElementById(
                "price"
            ).value
        );


    // Validation

    if (!productName) {

        alert("Please enter product name.");

        return;
    }


    if (
        !Number.isInteger(quantity) ||
        quantity <= 0
    ) {

        alert(
            "Quantity must be a whole number greater than 0."
        );

        return;
    }


    if (
        isNaN(price) ||
        price < 0
    ) {

        alert(
            "Please enter a valid price."
        );

        return;
    }


    products.push({

        product: productName,

        quantity: quantity,

        price: price

    });


    clearProductInputs();

    renderProducts();

    calculateTotals();

}


// ==========================================
// RENDER PRODUCTS
// ==========================================

function renderProducts() {

    const tbody =
        document.getElementById(
            "productTableBody"
        );


    tbody.innerHTML = "";


    if (products.length === 0) {

        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="empty-row">
                    No products added
                </td>
            </tr>
        `;

        return;
    }


    products.forEach(
        (item, index) => {

            const row =
                document.createElement("tr");


            if (
                selectedProductIndex === index
            ) {

                row.classList.add("selected");
            }


            row.innerHTML = `

                <td>${escapeHTML(item.product)}</td>

                <td>${item.quantity}</td>

                <td>Rs. ${item.price.toFixed(2)}</td>

                <td>
                    Rs. ${(item.quantity * item.price).toFixed(2)}
                </td>

            `;


            row.onclick = function () {

                selectedProductIndex = index;

                renderProducts();
            };


            tbody.appendChild(row);

        }
    );
}


// ==========================================
// EDIT SELECTED PRODUCT
// ==========================================

function editSelectedProduct() {

    if (selectedProductIndex === -1) {

        alert(
            "Please select a product from the table."
        );

        return;
    }


    const item =
        products[selectedProductIndex];


    document.getElementById(
        "productName"
    ).value = item.product;


    document.getElementById(
        "quantity"
    ).value = item.quantity;


    document.getElementById(
        "price"
    ).value = item.price;


    editingProductIndex =
        selectedProductIndex;


    document.getElementById(
        "addProductBtn"
    ).style.display = "none";


    document.getElementById(
        "editProductBtn"
    ).style.display = "none";


    document.getElementById(
        "updateProductBtn"
    ).style.display = "inline-block";
}


// ==========================================
// UPDATE PRODUCT
// ==========================================

function updateProduct() {

    if (editingProductIndex === -1) {

        return;
    }


    const productName =
        document.getElementById(
            "productName"
        ).value.trim();


    const quantity =
        Number(
            document.getElementById(
                "quantity"
            ).value
        );


    const price =
        Number(
            document.getElementById(
                "price"
            ).value
        );


    if (!productName) {

        alert(
            "Please enter product name."
        );

        return;
    }


    if (
        !Number.isInteger(quantity) ||
        quantity <= 0
    ) {

        alert(
            "Quantity must be greater than 0."
        );

        return;
    }


    if (
        isNaN(price) ||
        price < 0
    ) {

        alert(
            "Please enter a valid price."
        );

        return;
    }


    products[editingProductIndex] = {

        product: productName,

        quantity: quantity,

        price: price

    };


    selectedProductIndex =
        editingProductIndex;


    editingProductIndex = -1;


    resetProductButtons();

    clearProductInputs();

    renderProducts();

    calculateTotals();
}


// ==========================================
// REMOVE PRODUCT
// ==========================================

function removeSelectedProduct() {

    if (selectedProductIndex === -1) {

        alert(
            "Please select a product from the table."
        );

        return;
    }


    products.splice(
        selectedProductIndex,
        1
    );


    selectedProductIndex = -1;


    editingProductIndex = -1;


    resetProductButtons();

    renderProducts();

    calculateTotals();
}


// ==========================================
// RESET PRODUCT BUTTONS
// ==========================================

function resetProductButtons() {

    document.getElementById(
        "addProductBtn"
    ).style.display = "inline-block";


    document.getElementById(
        "editProductBtn"
    ).style.display = "inline-block";


    document.getElementById(
        "updateProductBtn"
    ).style.display = "none";
}


// ==========================================
// CLEAR PRODUCT INPUTS
// ==========================================

function clearProductInputs() {

    document.getElementById(
        "productName"
    ).value = "";


    document.getElementById(
        "quantity"
    ).value = "";


    document.getElementById(
        "price"
    ).value = "";
}


// ==========================================
// CALCULATE TOTALS
// ==========================================

function calculateTotals() {

    let subtotal = 0;


    products.forEach(
        item => {

            subtotal +=
                item.quantity *
                item.price;

        }
    );


    let gst =
        Number(
            document.getElementById(
                "gst"
            ).value
        );


    let discount =
        Number(
            document.getElementById(
                "discount"
            ).value
        );


    if (isNaN(gst)) {
        gst = 0;
    }


    if (isNaN(discount)) {
        discount = 0;
    }


    if (gst < 0) {
        gst = 0;
    }


    if (gst > 100) {
        gst = 100;
    }


    if (discount < 0) {
        discount = 0;
    }


    if (discount > 100) {
        discount = 100;
    }


    const discountAmount =
        subtotal *
        discount /
        100;


    const amountAfterDiscount =
        subtotal -
        discountAmount;


    const gstAmount =
        amountAfterDiscount *
        gst /
        100;


    const grandTotal =
        amountAfterDiscount +
        gstAmount;


    document.getElementById(
        "subtotal"
    ).textContent =
        `Rs. ${subtotal.toFixed(2)}`;


    document.getElementById(
        "discountAmount"
    ).textContent =
        `- Rs. ${discountAmount.toFixed(2)}`;


    document.getElementById(
        "gstAmount"
    ).textContent =
        `Rs. ${gstAmount.toFixed(2)}`;


    document.getElementById(
        "grandTotal"
    ).textContent =
        `Rs. ${grandTotal.toFixed(2)}`;
}


// ==========================================
// VALIDATE FORM
// ==========================================

function validateForm() {

    const company =
        document.getElementById(
            "companyName"
        ).value.trim();


    const customer =
        document.getElementById(
            "customerName"
        ).value.trim();


    const phone =
        document.getElementById(
            "phone"
        ).value.trim();


    const email =
        document.getElementById(
            "email"
        ).value.trim();


    const gst =
        Number(
            document.getElementById(
                "gst"
            ).value
        );


    const discount =
        Number(
            document.getElementById(
                "discount"
            ).value
        );


    if (!company) {

        alert(
            "Please enter company name."
        );

        return false;
    }


    if (!customer) {

        alert(
            "Please enter customer name."
        );

        return false;
    }


    if (!/^\d{10,15}$/.test(phone)) {

        alert(
            "Phone number must contain 10 to 15 digits."
        );

        return false;
    }


    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(email)) {

        alert(
            "Please enter a valid email address."
        );

        return false;
    }


    if (products.length === 0) {

        alert(
            "Please add at least one product."
        );

        return false;
    }


    if (
        isNaN(gst) ||
        gst < 0 ||
        gst > 100
    ) {

        alert(
            "GST must be between 0 and 100."
        );

        return false;
    }


    if (
        isNaN(discount) ||
        discount < 0 ||
        discount > 100
    ) {

        alert(
            "Discount must be between 0 and 100."
        );

        return false;
    }


    return true;
}


// ==========================================
// GENERATE PDF INVOICE
// ==========================================

async function generateInvoice() {

    if (!validateForm()) {

        return;
    }


    const company =
        document.getElementById(
            "companyName"
        ).value.trim();


    const customer =
        document.getElementById(
            "customerName"
        ).value.trim();


    const phone =
        document.getElementById(
            "phone"
        ).value.trim();


    const email =
        document.getElementById(
            "email"
        ).value.trim();


    const gst =
        Number(
            document.getElementById(
                "gst"
            ).value
        );


    const discount =
        Number(
            document.getElementById(
                "discount"
            ).value
        );


    const paymentMethod =
        document.getElementById(
            "paymentMethod"
        ).value;


    const paymentStatus =
        document.getElementById(
            "paymentStatus"
        ).value;


    // =====================================
    // CALCULATIONS
    // =====================================

    let subtotal = 0;


    products.forEach(
        item => {

            subtotal +=
                item.quantity *
                item.price;

        }
    );


    const discountAmount =
        subtotal *
        discount /
        100;


    const amountAfterDiscount =
        subtotal -
        discountAmount;


    const gstAmount =
        amountAfterDiscount *
        gst /
        100;


    const grandTotal =
        amountAfterDiscount +
        gstAmount;


    // =====================================
    // PDF
    // =====================================

    const {
        jsPDF
    } = window.jspdf;


    const doc =
        new jsPDF();


    const pageWidth =
        doc.internal.pageSize.getWidth();


    const pageHeight =
        doc.internal.pageSize.getHeight();


    const purple =
        [91, 33, 182];


    const lightPurple =
        [237, 233, 254];


    // =====================================
    // HEADER
    // =====================================

    doc.setFillColor(
        purple[0],
        purple[1],
        purple[2]
    );


    doc.roundedRect(
        10,
        10,
        pageWidth - 20,
        35,
        4,
        4,
        "F"
    );


    // Logo

    try {

        const logo =
            await loadImage(
                "logo.png"
            );


        if (logo) {

            doc.addImage(
                logo,
                "PNG",
                14,
                14,
                28,
                27
            );

        }

    } catch (error) {

        console.log(
            "Logo not found."
        );
    }


    doc.setTextColor(
        255,
        255,
        255
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.setFontSize(16);


    doc.text(
        "CHANDU TECHNOLOGIES",
        48,
        22
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(8);


    doc.text(
        "Innovate • Build • Grow",
        48,
        28
    );


    doc.text(
        email,
        48,
        34
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.setFontSize(17);


    doc.text(
        "INVOICE",
        pageWidth - 18,
        22,
        {
            align: "right"
        }
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(7);


    doc.text(
        document.getElementById(
            "invoiceNumber"
        ).textContent,
        pageWidth - 18,
        29,
        {
            align: "right"
        }
    );


    doc.text(
        document.getElementById(
            "invoiceDate"
        ).textContent,
        pageWidth - 18,
        35,
        {
            align: "right"
        }
    );


    // =====================================
    // BILL TO
    // =====================================

    doc.setTextColor(
        purple[0],
        purple[1],
        purple[2]
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.setFontSize(10);


    doc.text(
        "BILL TO",
        15,
        58
    );


    doc.setTextColor(
        0,
        0,
        0
    );


    doc.setFontSize(10);


    doc.text(
        customer,
        15,
        66
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(8);


    doc.text(
        "Phone: " + phone,
        15,
        72
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.text(
        company,
        pageWidth - 15,
        62,
        {
            align: "right"
        }
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(7);


    doc.text(
        "Invoice Generated by",
        pageWidth - 15,
        68,
        {
            align: "right"
        }
    );


    // =====================================
    // PRODUCT TABLE
    // =====================================

    const tableRows =
        products.map(
            item => [

                item.product,

                item.quantity,

                `Rs. ${item.price.toFixed(2)}`,

                `Rs. ${(item.quantity * item.price).toFixed(2)}`

            ]
        );


    doc.autoTable({

        startY: 82,

        head: [
            [
                "PRODUCT",
                "QTY",
                "PRICE",
                "TOTAL"
            ]
        ],

        body: tableRows,

        theme: "grid",

        styles: {

            fontSize: 8,

            cellPadding: 4,

            textColor: [
                30,
                30,
                30
            ]

        },

        headStyles: {

            fillColor: lightPurple,

            textColor: [
                76,
                29,
                149
            ],

            fontStyle: "bold"

        },

        columnStyles: {

            0: {
                cellWidth: 85
            },

            1: {
                cellWidth: 20,
                halign: "center"
            },

            2: {
                cellWidth: 35,
                halign: "right"
            },

            3: {
                cellWidth: 40,
                halign: "right"
            }

        },

        margin: {

            left: 15,

            right: 15

        }

    });


    // =====================================
    // SUMMARY
    // =====================================

    let summaryY =
        doc.lastAutoTable.finalY + 12;


    if (
        summaryY > pageHeight - 100
    ) {

        doc.addPage();

        summaryY = 20;
    }


    doc.setFillColor(
        245,
        243,
        255
    );


    doc.roundedRect(
        pageWidth - 85,
        summaryY,
        70,
        43,
        3,
        3,
        "F"
    );


    doc.setTextColor(
        0,
        0,
        0
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(8);


    doc.text(
        "Subtotal",
        pageWidth - 80,
        summaryY + 8
    );


    doc.text(
        `Rs. ${subtotal.toFixed(2)}`,
        pageWidth - 20,
        summaryY + 8,
        {
            align: "right"
        }
    );


    doc.text(
        `Discount (${discount}%)`,
        pageWidth - 80,
        summaryY + 17
    );


    doc.text(
        `- Rs. ${discountAmount.toFixed(2)}`,
        pageWidth - 20,
        summaryY + 17,
        {
            align: "right"
        }
    );


    doc.text(
        `GST (${gst}%)`,
        pageWidth - 80,
        summaryY + 26
    );


    doc.text(
        `Rs. ${gstAmount.toFixed(2)}`,
        pageWidth - 20,
        summaryY + 26,
        {
            align: "right"
        }
    );


    // =====================================
    // GRAND TOTAL
    // =====================================

    doc.setFillColor(
        purple[0],
        purple[1],
        purple[2]
    );


    doc.roundedRect(
        pageWidth - 80,
        summaryY + 31,
        65,
        10,
        2,
        2,
        "F"
    );


    doc.setTextColor(
        255,
        255,
        255
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.setFontSize(8);


    doc.text(
        "GRAND TOTAL",
        pageWidth - 76,
        summaryY + 38
    );


    doc.text(
        `Rs. ${grandTotal.toFixed(2)}`,
        pageWidth - 20,
        summaryY + 38,
        {
            align: "right"
        }
    );


    // =====================================
    // PAYMENT DETAILS
    // =====================================

    let paymentY =
        summaryY + 62;


    if (
        paymentY > pageHeight - 65
    ) {

        doc.addPage();

        paymentY = 25;
    }


    doc.setTextColor(
        purple[0],
        purple[1],
        purple[2]
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.setFontSize(9);


    doc.text(
        "PAYMENT DETAILS",
        15,
        paymentY
    );


    doc.setTextColor(
        0,
        0,
        0
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(8);


    doc.text(
        "Payment Method:",
        15,
        paymentY + 10
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.text(
        paymentMethod,
        50,
        paymentY + 10
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.text(
        "Payment Status:",
        15,
        paymentY + 20
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.text(
        paymentStatus,
        50,
        paymentY + 20
    );


    // =====================================
    // FOOTER
    // =====================================

    doc.setDrawColor(
        216,
        180,
        254
    );


    doc.line(
        15,
        pageHeight - 25,
        pageWidth - 15,
        pageHeight - 25
    );


    doc.setTextColor(
        100,
        100,
        100
    );


    doc.setFont(
        "helvetica",
        "bold"
    );


    doc.setFontSize(8);


    doc.text(
        "Thank you for your business!",
        pageWidth / 2,
        pageHeight - 17,
        {
            align: "center"
        }
    );


    doc.setFont(
        "helvetica",
        "normal"
    );


    doc.setFontSize(7);


    doc.text(
        "CHANDU TECHNOLOGIES • Smart Invoice Generator",
        pageWidth / 2,
        pageHeight - 10,
        {
            align: "center"
        }
    );


    // =====================================
    // DOWNLOAD
    // =====================================

    const invoiceNumber =
        document.getElementById(
            "invoiceNumber"
        ).textContent;


    doc.save(
        `${invoiceNumber}.pdf`
    );


    showStatus(
        "✅ Invoice generated successfully!",
        true
    );
}


// ==========================================
// LOAD LOGO
// ==========================================

function loadImage(src) {

    return new Promise(
        (resolve, reject) => {

            const img =
                new Image();


            img.onload = function () {

                resolve(img);
            };


            img.onerror = function () {

                reject(
                    new Error(
                        "Image not found"
                    )
                );
            };


            img.src =
                src +
                "?v=" +
                Date.now();

        }
    );
}


// ==========================================
// CLEAR FORM
// ==========================================

function clearForm() {

    document.getElementById(
        "companyName"
    ).value = "";


    document.getElementById(
        "customerName"
    ).value = "";


    document.getElementById(
        "phone"
    ).value = "";


    document.getElementById(
        "email"
    ).value =
        "chandusc253@gmail.com";


    document.getElementById(
        "gst"
    ).value = 18;


    document.getElementById(
        "discount"
    ).value = 0;


    document.getElementById(
        "paymentMethod"
    ).value = "Cash";


    document.getElementById(
        "paymentStatus"
    ).value = "Paid";


    products = [];


    selectedProductIndex = -1;


    editingProductIndex = -1;


    clearProductInputs();

    resetProductButtons();

    renderProducts();

    calculateTotals();

    updateInvoiceDetails();


    showStatus(
        "Form cleared.",
        false
    );
}


// ==========================================
// STATUS
// ==========================================

function showStatus(
    message,
    success
) {

    const status =
        document.getElementById(
            "statusMessage"
        );


    status.textContent = message;


    if (success) {

        status.style.color =
            "#16a34a";

    } else {

        status.style.color =
            "#5b21b6";
    }


    setTimeout(
        function () {

            status.textContent = "";

        },
        4000
    );
}


// ==========================================
// SECURITY
// ==========================================

function escapeHTML(text) {

    const div =
        document.createElement("div");


    div.textContent = text;


    return div.innerHTML;
}
