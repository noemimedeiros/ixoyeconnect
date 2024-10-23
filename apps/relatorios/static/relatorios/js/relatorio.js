function ministro_externo_local(){
    let ministro_externo = $('#id_ministro_externo').is(':checked');
        if(ministro_externo){
            $('#div_id_ministro').css('display', 'none')
            $('#div_id_ministro_texto').css('display', 'block')
        }else{
            $('#div_id_ministro').css('display', 'block')
            $('#div_id_ministro_texto').css('display', 'none')
        }
}
$('#id_ministro_externo').change(() => ministro_externo_local())

$(function(){
    ministro_externo_local()
})