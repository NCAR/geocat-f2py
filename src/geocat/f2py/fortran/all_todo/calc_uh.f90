!##################################################################
!##################################################################
!######                                                      ######
!######                  SUBROUTINE CALC_UH                  ######
!######                                                      ######
!######                     Developed by                     ######
!######     Center for Analysis and Prediction of Storms     ######
!######                University of Oklahoma                ######
!######                                                      ######
!##################################################################
!##################################################################
!
!  Calculates updraft helicity (UH) to detect rotating updrafts.
!  Formula follows Kain et al, 2008, Wea. and Forecasting, 931-952,
!  but this version has controls for the limits of integration
!  uhminhgt to uhmxhgt, in m AGL.  Kain et al used 2000 to 5000 m.
!  Units of UH are m^2/s^2.
!
!  Note here that us and vs are at ARPS scalar points.
!  w is at w-point (scalar pt in horiz, staggered vertical)
!
!  Keith Brewster, CAPS/Univ. of Oklahoma
!  March, 2010

!NCLFORTSTART
SUBROUTINE DCALCUH(nx, ny, nz, nzp1, zp, mapfct, dx, dy, uhmnhgt, uhmxhgt, us, &
                   vs, w, uh, tem1, tem2)

    IMPLICIT NONE

    !f2py threadsafe
    !f2py intent(in,out) :: uh

    INTEGER, INTENT(IN) :: nx, ny, nz, nzp1
    REAL(KIND=8), DIMENSION(nx,ny,nzp1), INTENT(IN)  :: zp
    REAL(KIND=8), DIMENSION(nx,ny), INTENT(IN) :: mapfct
    REAL(KIND=8), INTENT(IN) :: dx, dy
    REAL(KIND=8), INTENT(IN) :: uhmnhgt, uhmxhgt
    REAL(KIND=8), DIMENSION(nx,ny,nz), INTENT(IN)  :: us
    REAL(KIND=8), DIMENSION(nx,ny,nz), INTENT(IN)  :: vs
    REAL(KIND=8), DIMENSION(nx,ny,nzp1), INTENT(IN)  :: w
    REAL(KIND=8), DIMENSION(nx,ny), INTENT(OUT) :: uh
    REAL(KIND=8), DIMENSION(nx,ny,nz), INTENT(INOUT) :: tem1
    REAL(KIND=8), DIMENSION(nx,ny,nz), INTENT(INOUT) :: tem2

!NCLEND

    ! Misc local variables
    INTEGER :: i, j, k, kbot, ktop
    REAL(KIND=8) :: twodx, twody, wgtlw, sum, wmean, wsum !,wavg
    REAL(KIND=8) :: helbot, heltop, wbot, wtop
    REAL(KIND=8) :: zbot, ztop

    ! Initialize arrays
    uh = 0.0
    tem1 = 0.0

    ! Calculate vertical component of helicity at scalar points
    !   us: u at scalar points
    !   vs: v at scalar points

    twodx = 2.0*dx
    twody = 2.0*dy

    !$OMP PARALLEL

    !$OMP DO COLLAPSE(3) SCHEDULE(runtime)
    DO k=2,nz-2
        DO j=2,ny-1
            DO i=2,nx-1
                !wavg = 0.5*(w(i,j,k)+w(i,j,k+1))
                tem1(i,j,k) = (0.5*(w(i,j,k)+w(i,j,k+1)))*((vs(i+1,j,k) - &
                              vs(i-1,j,k))/(twodx*mapfct(i,j)) - &
                              (us(i,j+1,k) - us(i,j-1,k))/(twody*mapfct(i,j)))
                tem2(i,j,k) = 0.5*(zp(i,j,k) + zp(i,j,k+1))
            END DO
        END DO
    END DO
    !$OMP END DO

    ! Integrate over depth uhminhgt to uhmxhgt AGL
    !
    !  WRITE(6,'(a,f12.1,a,f12.1,a)') &
    !        'Calculating UH from ',uhmnhgt,' to ',uhmxhgt,' m AGL'
    !$OMP DO COLLAPSE(2) PRIVATE(i, j, k, zbot, ztop, kbot, ktop, &
    !$OMP wgtlw, wbot, wtop, wsum, wmean, sum, helbot, heltop) SCHEDULE(runtime)
    DO j=2,ny-2
        DO i=2,nx-2
            zbot = zp(i,j,2) + uhmnhgt
            ztop = zp(i,j,2) + uhmxhgt
            !
            ! Find wbar, weighted-mean vertical velocity in column
            ! Find w at uhmnhgt AGL (bottom)
            !
            DO k=2,nz-3
                IF(zp(i,j,k) > zbot) EXIT
            END DO
            kbot = k
            wgtlw = (zp(i,j,kbot) - zbot)/(zp(i,j,kbot) - zp(i,j,kbot-1))
            wbot = (wgtlw*w(i,j,kbot-1)) + ((1. - wgtlw)*w(i,j,kbot))

            ! Find w at uhmxhgt AGL (top)
            DO k=2,nz-3
                IF(zp(i,j,k) > ztop) EXIT
            END DO
            ktop = k
            wgtlw = (zp(i,j,ktop) - ztop)/(zp(i,j,ktop) - zp(i,j,ktop-1))
            wtop = (wgtlw*w(i,j,ktop-1)) + ((1. - wgtlw)*w(i,j,ktop))

            ! First part, uhmnhgt to kbot
            wsum = 0.5*(w(i,j,kbot) + wbot)*(zp(i,j,kbot) - zbot)

            ! Integrate up through column
            DO k=(kbot+1),(ktop-1)
                wsum = wsum + 0.5*(w(i,j,k) + w(i,j,k-1))*(zp(i,j,k) - zp(i,j,k-1))
            END DO

            ! Last part, ktop-1 to uhmxhgt
            wsum = wsum + 0.5*(wtop + w(i,j,ktop-1))*(ztop - zp(i,j,ktop-1))
            wmean = wsum/(uhmxhgt - uhmnhgt)

            IF (wmean > 0.) THEN    ! column updraft, not downdraft

                ! Find helicity at uhmnhgt AGL (bottom)
                DO k=2,nz-3
                    IF (tem2(i,j,k) > zbot) EXIT
                END DO
                kbot = k
                wgtlw = (tem2(i,j,kbot) - zbot)/(tem2(i,j,kbot) - tem2(i,j,kbot-1))
                helbot = (wgtlw*tem1(i,j,kbot-1)) + ((1. - wgtlw)*tem1(i,j,kbot))

                ! Find helicity at uhmxhgt AGL (top)
                DO k=2,nz-3
                    IF (tem2(i,j,k) > ztop) EXIT
                END DO
                ktop = k
                wgtlw = (tem2(i,j,ktop) - ztop)/(tem2(i,j,ktop) - tem2(i,j,ktop-1))
                heltop = (wgtlw*tem1(i,j,ktop-1)) + ((1. - wgtlw)*tem1(i,j,ktop))

                ! First part, uhmnhgt to kbot
                sum = 0.5*(tem1(i,j,kbot) + helbot)*(tem2(i,j,kbot) - zbot)

                ! Integrate up through column
                DO k=(kbot+1),(ktop-1)
                    sum = sum + 0.5*(tem1(i,j,k) + tem1(i,j,k-1))*(tem2(i,j,k) - tem2(i,j,k-1))
                END DO

                ! Last part, ktop-1 to uhmxhgt
                uh(i,j) = sum + 0.5*(heltop + tem1(i,j,ktop-1))*(ztop - tem2(i,j,ktop-1))
            END IF
        END DO
    END DO
    !$OMP END DO

    !$OMP END PARALLEL

    RETURN

END SUBROUTINE DCALCUH
