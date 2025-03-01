import { Component, inject } from '@angular/core';
import { AuthService } from '../../../services/auth.service';
import { Router, RouterModule } from '@angular/router';
import { FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  private readonly authService: AuthService = inject(AuthService);
  private readonly router = inject(Router);
  loginForm!: FormGroup;
  private _fb: FormBuilder = inject(FormBuilder);

  ngOnInit() {
    this.loginForm = this._fb.group({
      apiKey: new FormControl('', [Validators.required]),
    });
  }

  login() {
    if (this.loginForm.valid) {
      this.authService
        .login(this.loginForm.controls['apiKey'].value)
        .subscribe({
          next: () => {
            this.loginForm.reset();
            this.router.navigate(['/menu/list']);
          },
          error: (error) => {
            console.error('Autenticación fallida', error);
            this.loginForm.reset();
          },
        });
    }
  }
}
