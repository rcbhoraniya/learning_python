const addMoreBtn = document.getElementById('add-new-form')
const total = document.getElementById('id_form-TOTAL_FORMS').value
console.log(count)
const currentFormRow = document.getElementsByClassName('form-row')
const formCount=currentFormRow.length

for(i=0;i<formCount;i++){
    currentFormRow[i].setAttribute('id',`form-${i}`)
    }

addMoreBtn.addEventListener('click',add_new_form)

function add_new_form(event){
    if(event){
    event.preventDefault()
    }

    console.log(formCount)
//    // add new empty form element to our htmp form
    const formCopyTarget = document.getElementById('invoice-form-items-table-body')
    const newElement = document.getElementById(`form-${formCount-1}`).cloneNode(true)

    newElement.each(function() {
        var name = $(this).attr('name');
        console.log(name);
        if(name) {
            name = name.replace('-' + (total-1) + '-', '-' + total + '-');
                    console.log(name);

            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        }
    });
    newElement.find('label').each(function() {
        var forValue = $(this).attr('for');
        if (forValue) {
        forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
        $(this).attr({'for': forValue});
        }
    });
    total++;
    console.log(total-1)
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);




//    emptyFormEl.setAttribute('id',`form-${currentFormCount}`)
//    const regex = new RegExp('__prefix__','g')
//    emptyFormEl.innerHTML = emptyFormEl.innerHTML.replace(regex,currentFormCount)
//    totalNewForm.setAttribute('value',currentFormCount+1)
//    formCopyTarget.append(emptyFormEl)

    }