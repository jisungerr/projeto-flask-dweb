 function myFunction() {
        Swal.fire({
            title: 'Deseja apagar mesmo?',
            text: "Não será possível reverter isso.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#41d630',
            cancelButtonColor: '#d33',
            cancelButtonText: 'Cancelar',
            confirmButtonText: 'Deletar'
            }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire(
                  'Deletado!',
                  'O cadastro foi apagado',
                  'success'
                )
            }
        })
}
