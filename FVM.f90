Module shared
   Real*8, parameter  :: ytos = 3.15576d7, pctocm = 3.08568d18
   integer, parameter :: Rdim = 4000, Edim = 1001, Rcri = 50
   Real*8, parameter  :: gmin = 1d0, gmax = 1d9, dr = pctocm, D0 = 2.08d0, delta = 0.5d0, magfield = 7d-6
   Real*8 Tage, Dist, Edot, alpha
   Real*8, parameter  :: pi = 3.14159265358979323846d0, C = 29979245800.d0, ME = 9.10938188d-28, Eesu = 4.80320427d-10
!Real*8, parameter :: Mej=5.d0*msolar, rhoism=0.3d0*mu*massp, Esn=1d51, Emin=1d0, Emax=1.4d5,Tage=1.2d4*ytos,beta=-0.2d0
!Real*8 rch,vch,tch,rbb, vbb, rrs, vrs, tcoren, tstn, indsnr, Estep, t, Phi, xiacc, Ep
End Module Shared

PROGRAM Main
   use shared
   IMPLICIT NONE
   Real*8 Estep, dt, t, Q0, V1
   Real*8 E(Edim), D(Rdim, Edim), N(Rdim, Edim), R(Rdim + 1)
   integer ir, ie, nrp

   open(11,file='log',status="unknown")
   Read (5, *) Tage, Dist, Edot, alpha!Tage in s; Dist in pc; Edot in mec^2
   nrp = ifix(sngl(Dist))
   ! dt = 10d0*ytos
   dt = Tage / 200d0
   Do ir = 1, Rdim + 1
      R(ir) = dble(ir - 1)*dr
   End Do
   Estep = dexp(dlog(gmax/gmin)/dble(Edim - 1))
   E(1) = gmin
   Do ie = 1, Edim
      if (ie > 1) E(ie) = E(ie - 1)*Estep
      D(1:Rcri, ie) = 1d26*(E(ie)/1956.95d0)**0.33d0
      D(Rcri + 1:Rdim, ie) = D0*1d28*(E(ie)/1956.95d0)**delta
      N = 0d0

   End DO
   t = dt/2.d0
   V1 = 4.d0*pi/3.d0*R(2)**3
   Do while (t < Tage)
   do ie = 1, Edim
      N(1, ie) = N(1, ie) + Edot*(1.d0 + Tage/1d4/ytos)**2/(1.d0 + t/1d4/ytos)**2&
                &*(2.d0 - alpha)/(gmax**(2.d0 - alpha) - 1.d0)/V1*E(ie)**(-alpha)
   Enddo
!N(1,ie)=Q0/4.d0/pi/R(2)**3*E(ie)**(-2.2d0)
!N(2:Rdim,ie)=0.d0
   call FDMloss(R, E, N, dt/2.d0, Estep)
   call dif(R, D, N, dt, Rdim, Edim)
   call FDMloss(R, E, N, dt/2.d0, Estep)
   t = t + dt
   write (11, *) t/Tage
   call flush (11)
   End Do
   do ie = 1, Edim
      write (6, *) E(ie), N(nrp, ie)
   Enddo
   close(11)

END PROGRAM MAIN

Subroutine FDMloss(R, E, N, dt, Estep)
   use shared
   implicit none
   Real*8 r0, tcs, p2, Estep
   Real*8 E(Edim), N(Rdim, Edim), R(Rdim + 1)
   Real*8 dE, blp, bl, dt
   Real*8 ae(Edim), be(Edim), ce(Edim), re(Edim), ue(Edim)
   integer ir, ie
   r0 = Eesu*Eesu/(ME*C*C)
   tcs = 8.d0*PI/3.d0*r0*r0
   p2 = -4.d0/3.d0*tcs/(ME*C)*magfield**2/8.d0/pi
   Do ir = 1, Rdim
      Do ie = 1, Edim
         blp = p2*(E(ie)*Estep)**2
         bl = p2*E(ie)**2
         dE = E(ie)*Estep - E(ie)
! ae(ie)=-0.d0
! be(ie)=+1.d0
! ce(ie)=-(blp*dt+dE)/(bl*dt-dE)
! re(ie)=-(bl*dt+dE)/(bl*dt-dE)*N(ir,ie)
!if(ie<Edim) re(ie)=re(ie)+(blp*dt-dE)/(bl*dt-dE)*N(ir,ie+1)
         ae(ie) = 0.d0
         be(ie) = 1.d0 - dt*p2*e(ie)**2/dE
         ce(ie) = dt*p2*e(ie)**2/dE
         re(ie) = N(ir, ie)
      End Do

      call tridag(ae, be, ce, re, ue, Edim)
      do ie = 1, Edim
         N(ir, ie) = ue(ie)
      enddo

   End Do!ir

   N(:, Edim) = 0.d0
   N(Rdim, :) = 0.d0

End Subroutine fdmloss

Subroutine dif(R, D, N, dt, Rdim, Edim)
   Implicit None
   integer Edim, Rdim
   Real*8 dt, dx1, dx2, Rp3mRm3, Const
   Real*8 D(Rdim + 1, Edim), N(Rdim, Edim), R(Rdim + 1)
   Real*8 aa(Rdim), bb(Rdim), cc(Rdim), rr(Rdim), uu(Rdim)
   integer ir, ie
   Do ie = 1, Edim
      dx2 = (R(3) - R(1))/2.d0
      Const = 3.d0*R(2)**2*D(2, ie)/(R(2)**3 - R(1)**3)/dx2*dt
      aa(1) = +0.d0
      bb(1) = +1.d0 + Const/2.d0
      cc(1) = -Const/2.d0
      rr(1) = +Const/2.d0*N(2, ie)&
    &+ (+1.d0 - Const/2.d0)*N(1, ie)

      dx1 = (R(Rdim + 1) - R(Rdim - 1))/2.d0
      Const = 3.d0*R(Rdim)**2*D(Rdim, ie)*dt/dx1/(R(Rdim + 1)**3 - R(Rdim)**3)
      aa(Rdim) = -Const/2.d0
      bb(Rdim) = +1.d0 + Const/2.d0
      cc(Rdim) = -0.d0
      rr(Rdim) = +Const/2.d0*N(Rdim - 1, ie)&
    &+ (+1.d0 - Const/2.d0)*N(Rdim, ie)

      Do ir = 2, Rdim - 1
         dx1 = (R(ir + 1) - R(ir - 1))/2.d0
         dx2 = (R(ir + 2) - R(ir))/2.d0
         Rp3mRm3 = R(ir + 1)**3 - R(ir)**3
         aa(ir) = -3.d0/2.d0*D(ir, ie)*R(ir)**2*dt/dx1/Rp3mRm3

         bb(ir) = +1.d0&
        &       + 3.d0/2.d0*D(ir + 1, ie)*R(ir + 1)**2*dt/dx2/Rp3mRm3&
        &       + 3.d0/2.d0*D(ir, ie)*R(ir)**2*dt/dx1/Rp3mRm3

         cc(ir) = -3.d0/2.d0*D(ir + 1, ie)*R(ir + 1)**2*dt/dx2/Rp3mRm3

         rr(ir) = +3.d0/2.d0*D(ir + 1, ie)*R(ir + 1)**2*dt/dx2/Rp3mRm3*N(ir + 1, ie)&
        &       + (1.d0 - 3.d0/2.d0*D(ir + 1, ie)*R(ir + 1)**2*dt/dx2/Rp3mRm3&
        &           - 3.d0/2.d0*D(ir, ie)*R(ir)**2*dt/dx1/Rp3mRm3)*N(ir, ie)&
        &       + 3.d0/2.d0*D(ir, ie)*R(ir)**2*dt/dx1/Rp3mRm3*N(ir - 1, ie)
      End Do

      call tridag(aa, bb, cc, rr, uu, Rdim)
      do ir = 1, Rdim
         if (uu(ir) .lt. -1d0) write (11, *) uu(ir)
         N(ir, ie) = uu(ir)
      enddo
   End Do
END subroutine

subroutine tridag(a, b, c, r, u, n)
   double precision a(n), b(n), c(n), r(n), u(n)
   parameter(NMAX=5000)
   double precision gam(NMAX), bet

   if (n > NMAX) then
      write (11, *) " tridag ... n>NMAX"
      return
   endif
   if (b(1) == 0.) then
      write (11, *) " tridag ... rewrite equations"
      return
   endif
   bet = b(1)
   u(1) = r(1)/bet
   do j = 2, n
      gam(j) = c(j - 1)/bet
      bet = b(j) - a(j)*gam(j)
      if (bet == 0.) then
         write (11, *) a(11), b(11), c(11)
         write (11, *) a(500), b(500), c(500)
         write (11, *) " tridag ... tridag failed"
         stop
         return
      endif
      u(j) = (r(j) - a(j)*u(j - 1))/bet
   enddo
   do j = n - 1, 1, -1
      u(j) = u(j) - gam(j + 1)*u(j + 1)
   enddo
   return
end
