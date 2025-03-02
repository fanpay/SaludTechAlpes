import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Solicitud } from '../../../core/solicitud.interface';
import { Subscription } from 'rxjs';
import { CreateService } from '../../../services/create.service';
import Swal from 'sweetalert2';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-create',
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './create.component.html',
  styleUrl: './create.component.css',
})
export class CreateComponent implements OnInit, OnDestroy {
  private readonly createService: CreateService = inject(CreateService);
  private solicitudSubscription: Subscription = new Subscription();
  private _fb: FormBuilder = inject(FormBuilder);
  private readonly router = inject(Router);
  solicitudForm!: FormGroup;

  ngOnInit(): void {
    this.solicitudForm = this._fb.group({
      usuario: ['', Validators.required],
      nombre_paciente: ['', Validators.required],
      cedula: ['', Validators.required],
      descripcion: ['', Validators.required],
      metadatos: this._fb.group({
        modalidad: ['', Validators.required],
        region: ['', Validators.required],
        resolucion: this._fb.group({
          alto: [null, [Validators.required, Validators.min(1)]],
          ancho: [null, [Validators.required, Validators.min(1)]],
          dpi: [null, [Validators.required, Validators.min(1)]],
        }),
        fecha_adquisicion: ['', Validators.required],
      }),
      configuracion: this._fb.group({
        nivel_anonimizacion: [null, Validators.required],
        formato_salida: ['', Validators.required],
        ajustes_contraste: this._fb.group({
          brillo: [
            null,
            [Validators.required, Validators.min(0), Validators.max(100)],
          ],
          contraste: [
            null,
            [Validators.required, Validators.min(0), Validators.max(100)],
          ],
        }),
        algoritmo: ['', Validators.required],
      }),
      referencia_entrada: this._fb.group({
        nombre_bucket: ['', Validators.required],
        llave_objeto: ['', Validators.required],
        proveedor_almacenamiento: ['', Validators.required],
      }),
    });
  }

  crearSolicitud() {
    if (this.solicitudForm.invalid) {
      console.error('Error el formulario no es válido');
      return;
    }

    const nuevaSolicitud = {
      ...this.solicitudForm.value,
    } as Solicitud;

    this.solicitudSubscription = this.createService
      .crearSolicitud(nuevaSolicitud)
      .subscribe({
        next: () => {
          Swal.fire({
            title: '¡Muy bien!',
            text: `Has creado la solicitud exitosamente`,
            icon: 'success',
            confirmButtonText: 'Ok',
          });
          this.solicitudForm.reset();
          this.router.navigate(['/menu/list'])
        },
        error: (error) => {
          Swal.fire({
            title: 'Oops...',
            text: `Ocurrió un error, no se creó la solicitud. Intente nuevamente.`,
            icon: 'error',
            confirmButtonText: 'Continuar',
          });
          console.error('Error al crear la solicitud', error);
        },
      });
  }

  ngOnDestroy(): void {
    if (this.solicitudSubscription) {
      this.solicitudSubscription.unsubscribe();
    }
  }
}
