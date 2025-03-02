import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ListService } from '../../../services/list.service';
import { Solicitud } from '../../../core/detail.interface';
import { Subscription, take } from 'rxjs';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-list',
  imports: [RouterModule],
  templateUrl: './list.component.html',
  styleUrl: './list.component.css'
})
export class ListComponent {
  private solicitudSubscription: Subscription = new Subscription();
  solicitudesData!: Solicitud[];
  #listService = inject(ListService);
  ngOnInit(): void {
    this._fetchDetails();
  }

  private _fetchDetails(): void {
    this.solicitudSubscription = this.#listService
      .getListByUser()
      .pipe(take(1))
      .subscribe({
        next: (response: { state: Solicitud[] }) => {
          this.solicitudesData = response.state;
        },
        error: (error) => {
          Swal.fire({
            title: 'Oops...',
            text: `Ocurrió un error, no se pudo obtener el listado del usuario.`,
            icon: 'error',
            confirmButtonText: 'Continuar',
            timer: 6000,
          });
          console.error('Error al listar ', error);
        },
      });
  }
}
