// Adicionar arquivos ao clicar no botão
const div_arquivospost = $('#div_arquivospost');
const lista_arquivospost = $('#lista_arquivos_post');
const totalFormsInput = $('#id_form-TOTAL_FORMS');

const icons_arquivos = (ext) => {
    switch(ext){
        case 'png': case 'jpg': case 'jpeg': case 'webp': case 'svg': case 'gif':
            return 'fa-image text-danger'
        case 'xls': case 'xlsx':
            return 'fa-file-excel text-success'
        case 'doc': case 'docx':
            return 'fa-file-word text-info'
        case 'pdf':
            return 'fa-file-pdf text-danger'
        case 'zip': case 'rar': case 'Z': case 'tar': case 'gz':
            return 'fa-file-zipper text-muted'
        case 'csv':
            return 'fa-file-csv text-success'
        case 'ppt': case 'pptm': case 'pptx':
            return 'fa-file-powerpoint text-warning'
        case 'mp3': case 'wav': case 'wma':
            return 'fa-file-audio text-danger'
        case 'mp4': case 'mov': case 'avi': case 'mpg': case 'wmv':
            return 'fa-file-video text-danger'
        default:
            return 'fa-file text-info'
    }
}


function adicionar_arquivo(file_name, id=null){
    $(`#arquivo_${arquivo_index}`).append(`
        <div id="id_arquivo_${arquivo_index}" class="arquivopost_card">
            <div class="arquivopost_body">
                <i class="fa-solid ${icons_arquivos(file_name.split('.').pop())}"></i>
                <span class="arquivopost_nome">
                    ${file_name}
                </span>
            </div>
            <div><i role="button" class="fa-solid fa-xmark fa-lg" onclick="remover_arquivo(${arquivo_index}, '${id}')"></i></div>
        </div>`
    )
    $(`[for="adicionar_arquivo_${arquivo_index}"]`).css('display', 'none')

    arquivo_index += 1;
    let new_field = `
        <div id="arquivo_${arquivo_index}">
            <input type="file" name="form-${arquivo_index}-arquivo" id="adicionar_arquivo_${arquivo_index}" hidden>
        </div>
    `;

    let new_button = `
    <label for="adicionar_arquivo_${arquivo_index}" class="btn button-outlined button-upload">Anexar arquivo</label>
    `;

    div_arquivospost.append(new_field)
    lista_arquivospost.append(new_button)

    // A partir daqui, funcionamento do formset
    var totalForms = parseInt(totalFormsInput.val());
    totalFormsInput.val(totalForms + 1);

    $('[name$="-arquivo"]').on('change', function(){
        let id = $(this).prop('id');
        let file = document.getElementById(id).files.item(0);
        let file_name = file.name;
    
        adicionar_arquivo(file_name)
    })
}

$('[name$="-arquivo"]').on('change', function(){
    let id = $(this).prop('id');
    let file = document.getElementById(id).files.item(0);
    let file_name = file.name;

    adicionar_arquivo(file_name)
})

// Deletar arquivos adicionados
function remover_arquivo(arquivo, id=null){
    if(id != 'null'){
        if ($(`#arquivo_a_excluir_${arquivo}`).length > 0){
            $(`#id_arquivo_${arquivo}`).find('.fa-rotate-left').removeClass('fa-rotate-left').addClass('fa-xmark')
            $(`#id_arquivo_${arquivo}`).removeClass('border border-danger')
            $(`#arquivo_a_excluir_${arquivo}`).remove()
        }else{
            $('#arquivos-a-excluir').append(`<input id="arquivo_a_excluir_${arquivo}" type="hidden" name="arquivo_a_excluir" value="${id}"/>`)
            $(`#id_arquivo_${arquivo}`).addClass('border border-danger')
            $(`#id_arquivo_${arquivo}`).find('.fa-xmark').removeClass('fa-xmark').addClass('fa-rotate-left')
        }
    }else{
        $(`#arquivo_${arquivo}`).remove()
    }
}