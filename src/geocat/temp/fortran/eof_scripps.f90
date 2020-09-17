! NCLFORTSTART
subroutine deof11(d, nx, nt, nmodes, icovcor, dmsg, &
		&eigenvalues, eigenvectors, variance, &
		&princomp)
	! minimal argument list
	implicit none

	integer    nx, nt, nmodes, icovcor
	double precision d(nx, nt), eigenvalues(nmodes), &
			&eigenvectors(nx, nmodes), variance(nmodes)
	double precision princomp(nt, nmodes), dmsg
	! NCLEND
	integer iminnxnt, imaxnxnt
	integer n

	! need  iminnxnt and imaxnxnt for automatic allocation

	iminnxnt = min(nx, nt)
	imaxnxnt = max(nx, nt)

	call deof22(d, nx, nt, nmodes, icovcor, dmsg, &
			&eigenvalues, eigenvectors, variance, &
			&iminnxnt, imaxnxnt, princomp)

	return
end
! ----------------------------------------------------------------
subroutine deof22(d, nx, nt, nmodes, icovcor, dmsg, &
		&eigenvalues, eigenvectors, variance, &
		&iminnxnt, imaxnxnt, princomp)
	implicit none

	integer nx, nt, nmodes, icovcor, iminnxnt, imaxnxnt
	double precision d(nx, nt), eigenvalues(nmodes), &
			&eigenvectors(nx, nmodes), variance(nmodes)
	double precision princomp(nt, nmodes), dmsg

	! local and  automatic arrays
	double precision cumvariance(nmodes), &
			&spacked(iminnxnt * (iminnxnt + 1) / 2), evals(iminnxnt), &
			&evecs(iminnxnt, nmodes), rlawork(8 * iminnxnt), &
			&tentpcs(imaxnxnt, nmodes)
	double precision  sqrootweights(nx)
	integer ilawork(5 * iminnxnt), ifail(iminnxnt)
	integer n

	! NCL expects the user will do weighting externally

	do n = 1, nx
		sqrootweights(n) = 1.d0
	end do

	call deof(d, nx, nt, nmodes, icovcor, dmsg, &
			&eigenvalues, eigenvectors, princomp, variance, cumvariance, &
			&iminnxnt, imaxnxnt, spacked, evals, evecs, rlawork, &
			&ilawork, ifail, tentpcs, sqrootweights)
	return
end
! ----------------------------------------------------------------
! --- Original Scripps Code: modified for missing values [dmsg]
! ---                        Dennis Shea [Aug 2005]
! ----------------------------------------------------------------
subroutine deof(data, nx, nt, nmodes, icovcor, dmsg, &
		&eigenvalues, eigenvectors, princomp, variance, cumvariance, &
		&iminnxnt, imaxnxnt, spacked, evals, evecs, rlawork, &
		&ilawork, ifail, tentpcs, sqrootweights)

	!	------------------------------------------------------------------
	!	This routine generates the Empirical Orthogonal Functions (EOFs)
	!	for a given time-space data set.  (Note that although the routine
	!	is set up as if the data is exactly two dimensional (X,T), that
	!	you can compute the EOFs of 3-D (X,Y,T) fields simply by concat-
	!	enating the data along the X,Y axes into one big 2-D array and
	!	then computing the EOFs of that 2-D array).  The "typical"
	!	normalization is applied, i.e., the magnitude of the eigenvectors
	!	is scaled to be equal to 1.
	!
	!	David W. Pierce
	!	dpierce@ucsd.edu
	!	Scripps Institution of Oceanography
	!	Climate Research Division, 0224
	!	Jan 29, 1996
	!
	!	Inputs:
	!
	!		data(nx,nt): data to compute the EOFs of.  THIS MUST
	!			BE ANOMALIES.
	!
	!		nx, nt: number of space (nx) and time (nt) points in the
	!			input data array.
	!
	!		nmodes: number of modes (EOFs) to compute.
	!
	!		icovcor: if =0, then compute using covariance matrix;
	!			 if =1, then compute using correlation matrix.
	!			See, for example, discussion in Daniel S. Wilks
	!			1995, "Statistical Methods in the Atmospheric
	!			Sciences", p. 383 for a discussion.
	!
	!		iminnxnt: the SMALLER of 'nx' and 'nt'.
	!
	!		imaxnxnt: the LARGER of 'nx' and 'nt'.
	!
	!		spacked(iminnxnt*(iminnxnt+1)/2): workspace.  This is used to
	!			store the packed covariance or correlation matrix.
	!
	!		evals(iminnxnt): workspace.  This is used to store the
	!			complete series of eigenvalues.  I suppose you
	!			could access this if you wanted to, remembering
	!			that a) it's more modes than you asked for; b)
	!			they are in ASCENDING order rather than descending.
	!
	!		evecs(iminnxnt,nmodes): workspace.  This is used to store
	!			the (possibly switched) eigenvectors, which are
	!			in ascending order.
	!
	!		rlawork(8*iminnxnt): Real LAPACK workspace.
	!
	!		ilawork(5*iminnxnt): Integer LAPACK workspace.
	!
	!		ifail(iminnxnt): Integer LAPACK workspace.  This is used
	!			to indicate which eigenvectors didn't converge,
	!			if that happened.
	!
	!		tentpcs(imaxnxnt,nmodes): Real workspace.  This is
	!			used to store the 'tentative' principal components.
	!
	!		sqrootweights(nx) : NOT USED IN NCL IMPLEMENTATION [set to 1.0]
	!                       the SQUARE ROOT of the areal weighting to
	!			use.  Just set this to all 1.0's if you don't care
	!			about areal weighting.  I think you can set places
	!			which should be ignored to zero to have them not
	!			participate in the calculation, thus implementing a
	!			crude form of data masking.
	!
	!               dmsg    missing code
	!
	!	Outputs:
	!
	!		eigenvalues(nmodes): the computed eigenvalues of
	!			the data, the largest returned first.
	!
	!		eigenvectors(nx,nmodes): the computed eigenvectors
	!			of the data, the most important returned first.
	!
	!		princomp(nt,nmodes): the principal components of
	!			the data.
	!
	!		variance(nmodes): the percent of variance explained
	!			by each mode.
	!
	!		cumvariance(nmodes): the cumulative percent of
	!			variance explained by each mode.  This is
	!			a bit redundant -- it's just the sum
	!			of "variance".
	!
	!	Method:
	!
	!	EOFs are simply the eigenvectors of the covariance (or correlation)
	!	matrix.  So form the proper matrix from the data and pass it to
	!	a LAPACK routine which calculates eigenvectors/eigenvalues.  Then
	!	calculate the principal components explicitly using the fact that
	!	the principal component for mode M at time T is just the projection
	!	of the data at time T onto eigenvector M.
	!
	!	There is a slight complication for efficiency's sake.  That is,
	!	we often have nx >> nt, i.e., there are many more spatial than
	!	temporal points.  The traditional correlation/covariance matrix
	!	is size (nx,nx), which can be huge.  Think, for example, of a 3-D
	!	field of size (100,100,120) which has been concatenated into a
	!	2-D field of size (10000,120).  The traditional covariance/correlation
	!	matrix in this case is size (10000,10000)!  That's way too big to
	!	easily work with.  So, following the discussion in Preisendorfer
	!	(1988, "Principal Component Analysis in Meteorology and Oceanography",
	!	p. 64) we work, in such cases, in the "dual" of the space.  All
	!	that means is that we logically switch X and T; the
	!	covariance/correlation matrix for the example given above is then
	!	size (120,120), which is much easier and more efficient to work
	!	with.  If you do this kind of switch, the basic idea is that
	!	the eigenvectors of the switched matrix are the principal components
	!	of the original matrix, and the principal components of the switched
	!	matrix are the eigenvectors of the original matrix.  Which is to
	!	say, if you switch T and X to begin with, the final result is that
	!	the T dependence is in the X part and the X dependence is in the
	!	T part.  There is also a normalization which has to be applied--
	!	see Preisendorfer for details.
	!	------------------------------------------------------------------

	implicit none

	integer    covariance, correlation
	parameter(covariance = 0, correlation = 1)  ! possible values of 'icovcor'

	!	-----------------
	!	Passed parameters
	!	-----------------
	integer    nx, nt, nmodes, icovcor, iminnxnt, imaxnxnt
	integer ifail(iminnxnt)
	double precision data(nx, nt), eigenvalues(nmodes), &
			&eigenvectors(nx, nmodes), princomp(nt, nmodes), &
			&variance(nmodes), cumvariance(nmodes), &
			&spacked(iminnxnt * (iminnxnt + 1) / 2), evals(iminnxnt), &
			&evecs(iminnxnt, nmodes), rlawork(8 * iminnxnt), &
			&tentpcs(imaxnxnt, nmodes), sqrootweights(nx)
	double precision dmsg, deps
	integer ilawork(5 * iminnxnt)

	!	---------------
	!	Local variables
	!	---------------
	logical        doswitched
	integer        orderofs, i, j, jascending, jdescending
	double precision sum, fact, totvar
	character*1    jobz, range, uplo    ! for LAPACK routine
	integer        m, n, il, iu, ldz, info    ! for LAPACK routine
	double precision vl, vu, abstol        ! for LAPACK routine
	integer    lwork, mode

	logical DEBUG
	DEBUG = .false.

	if (DEBUG) then
		!print *, 'entering deof with nx, nt, nmodes=', nx, nt, nmodes
		!print *, 'sqrootweights:',sqrootweights(1:10)
	end if

	!	----------------------------------------------
	!	Weight the data by the square root of the area
	!	----------------------------------------------
	do j = 1, nt
		do i = 1, nx
			if (data(i, j).ne.dmsg) then
				data(i, j) = data(i, j) * sqrootweights(i)
			end if
		end do
	end do

	!	---------------------------------------------------------
	!	Figure out whether we should do the 'regular' EOF or the
	!	one with switched X and T axes.  The correlation matrix
	!	for the regular method is size (nx,nx) and for the
	!	switched method it is size (nt,nt); choose based on which
	!	of these is smaller.
	!	---------------------------------------------------------
	if (DEBUG) then
		!print *, 'figuring switched or not'
	end if

	doswitched = (nx .gt. nt)
	if(doswitched) then
		orderofs = nt
		!if (DEBUG) print *, 'deof: Working in switched mode'
	else
		orderofs = nx
		!if (DEBUG) print *, 'deof: Working in unswitched mode'
	endif
	if(orderofs .gt. iminnxnt) then
		!print *, 'Error!  EOF routine must be supplied '
		!print *, 'with enough workspace; passed parameter'
		!print *, 'iminnxnt must be at least ', orderofs
		!print *, 'Passed value was iminnxnt=', iminnxnt
		stop 'eof '
	endif
	if(nmodes .gt. orderofs) then
		!print *, 'Error! EOF routine called requesting more'
		!print *, 'modes than exist!  Request=', nmodes, ' exist=', &
		!&orderofs
		stop 'eof '
	endif

	!	-------------------------------------------------
	!	Form the covariance or correlation matrix, put it
	!	into 's'.  Note that 's' is always symmetric --
	!	the correlation between X and Y is the same as
	!	between Y and X -- so use packed storage for 's'.
	!	The packed storage scheme we use is the same as
	!	LAPACK uses so we can pass 's' directly to the
	!	solver routine: the matrix is lower triangular,
	!	and s(i,j) = spacked(i+(j-1)*(2*n-j)/2).
	!	-------------------------------------------------
	call deofcovcor(data, nx, nt, icovcor, covariance, &
			&correlation, spacked, doswitched, iminnxnt, dmsg)
	!	------------------------------------------------------
	!	Now call the LAPACK solver to get the eigenvalues
	!	and eigenvectors.  The eigenvalues express the
	!	amount of variance explained by the various modes,
	!	so choose to return those 'nmodes' modes which
	!	explain the most variance.
	!	Dims of arrays:
	!		evals  (n)	  ! The calculated eigenvalues
	!		evecs  (n,nmodes) ! The calculated eigenvectors
	!		rlawork(8*n)
	!		ilawork(5*n)
	!		ifail  (n)
	!	Remember that the calculated eigenvectors may not be
	!	the ones we really want if we are doing switched
	!	X and T axes.  However the eigen*values* are the same
	!	either way, according to Preisendorfer.
	!	*NOTE* that the LAPACK routine returns the eigenvalues
	!	(and corresponding eigenvectors) in ASCENDING order,
	!	but this routine returns them in DESCENDING order;
	!	this will be switched in the final assembly phase,
	!	below.
	!	------------------------------------------------------
	jobz = 'V'    ! Both eigenvalues and eigenvectors
	range = 'I'    ! Specify range of eigenvalues to get.
	uplo = 'L'    ! 'spacked' has lower triangular part of s
	n = orderofs
	il = n - nmodes + 1    ! Smallest eigenvalue to get
	iu = n        ! Largest eigenvalue to get
	abstol = 0.0d0        ! See LAPACK documentation
	ldz = n

	lwork = 8 * iminnxnt

	do j = 1, nmodes
		evals(j) = 0.0d0
		do i = 1, iminnxnt
			evecs(i, j) = 0.0d0
		end do
	end do

	if (DEBUG) then
		!print *,'about to call dspevx, spacked=', spacked(1:10)
		!print *,'about to call dspevx, spacked=',(spacked(i),i=1,10)
		do i = 1, 10
			!print *, "spacked: n=", n, "  ", spacked(i)
		end do
	end if

	call dspevx(jobz, range, uplo, n, spacked, &
			&vl, vu, il, iu, abstol, m, evals, evecs, ldz, &
			&rlawork, ilawork, ifail, info)

	!	------------------------------
	!	Check for LAPACK routine error
	!	------------------------------
	if(info .ne. 0) then
		if(info .lt. 0) then
			!print *, 'LAPACK error: argument ', &
			!&-info, ' had illegal value'
			stop 'eof'
		else
			!print *, 'LAPACK error: ', info, &
			!&'eigenvectors failed to converge!'
			!print *, 'Consult the LAPACK docs!'
			stop 'eof'
		endif
	endif

	!	------------------------------------------------
	!	Make sure that no eigenvalues <= zero.  Besides
	!	being mathematically forbidden, this would cause
	!	a divide by zero or negative sqrt error later on.
	!
	!       In the original code, it would exit if there was
	!       an eigenvalue less than 0. For our purposes, however,
	!       we'll just set the eigenvalue to 0 and let it continue.
	!	------------------------------------------------
	DEPS = 1d-6
	do i = 1, nmodes
		if(abs(evals(i)) .le. DEPS) then
			!print *, 'Error! LAPACK routine returned'
			!print *, 'eigenvalue <= 0!! ', i, evals(i)
			!print *, 'Warning! LAPACK routine returned eigenvalue <= 0.'
			!print *, 'Setting it to zero...'
			evals(i) = 0.0d0
			!do j=1, nmodes
			!print *, j, evals(j)
			!end do
			!print *, 'Note1: This means you may be asking'
			!print *, 'for more modes than the data supports.'
			!print *, 'Try reducing the number of requested'
			!print *, 'modes.'
			!print *, 'Note2: missing values can'
			!print *, 'result in a covariance matrix that'
			!print *, 'is not positive definite.'
			!stop 'eofunc'
		endif
	end do

	!	------------------------------------------------
	!	Compute the tentative principal components; they
	!	are 'tentative' because they might be the PCs
	!	of the switched data.  Put them into 'tentpcs',
	!	which is of size (nt,nmodes) if we are doing
	!	regular EOFs and (nx,nmodes) if we are doing
	!	switched EOFs.  These PCs come out in order
	!	corresponding to the order of 'evecs', which is
	!	in ASCENDING order.
	!	------------------------------------------------
	call deofpcs(data, nx, nt, nmodes, iminnxnt, &
			&imaxnxnt, evecs, doswitched, tentpcs, dmsg)

	!	--------------------------------------------------
	!	Now we have all the pieces to assemble our final
	!	result.  How we actually assemble them depends on
	!	whether we are doing switched or unswitched EOFs
	!	(except for the eigenVALUES, which are the same
	!	either way).
	!	--------------------------------------------------
	if(doswitched) then
		!		------------------------------------------
		!		In this case we must switch the principal
		!		components and the eigenvectors, applying
		!		the proper normalization.
		!		First get the unswitched eigenvectors,
		!		which are the switched (tentative) principal
		!		components divided by the square root of the
		!		appropriate eigenvalue.  Recall that the
		!		LAPACK values are in ASCENDING order while
		!		we want them in DESCENDING order; do the
		!		switch in this loop.
		!		--------------------------------------------
		do jascending = 1, nmodes
			jdescending = nmodes - jascending + 1
			if(abs(evals(jascending)) .le. DEPS) then
				fact = 0.0d0
			else
				fact = 1.0d0 / sqrt(evals(jascending))
			end if
			do i = 1, nx
				eigenvectors(i, jdescending) = &
						&tentpcs(i, jascending) * fact
			end do
		end do

		!		-----------------------------------------------
		!		Next get unswitched principal components, which
		!		are the switched eigenvectors multiplied by
		!		the appropriate eigenvalues.
		!		-----------------------------------------------
		do jascending = 1, nmodes
			jdescending = nmodes - jascending + 1
			fact = sqrt(evals(jascending))
			do i = 1, nt
				princomp(i, jdescending) = &
						&evecs(i, jascending) * fact
			end do
		end do
	else
		!		-------------------------------------------------
		!		This is the unswitched case, and so it is easier.
		!		All we have to do is return things in DESCENDING
		!		order despite the fact that LAPACK returns them
		!		in ASCENDING order.
		!		Do the eigenvectors first...
		!		-------------------------------------------------
		do jascending = 1, nmodes
			jdescending = nmodes - jascending + 1
			do i = 1, nx
				eigenvectors(i, jdescending) = &
						&evecs(i, jascending)
			end do
		end do

		!		--------------------------------
		!		...then the principal components
		!		--------------------------------
		do jascending = 1, nmodes
			jdescending = nmodes - jascending + 1
			do i = 1, nt
				princomp(i, jdescending) = &
						&tentpcs(i, jascending)
			end do
		end do

	endif

	!	--------------------------------------------
	!	Do the second half of the areal weighting...
	!	--------------------------------------------
	do mode = 1, nmodes
		do i = 1, nx
			if(sqrootweights(i) .eq. 0.0d0) then
				eigenvectors(i, mode) = 0.0d0
			else
				eigenvectors(i, mode) = &
						&eigenvectors(i, mode) / sqrootweights(i)
			endif
		end do
	end do

	!	------------------------------------------------
	!	Scale the eigenvectors to have a magnitude of 1;
	!	scale the corresponding principal components to
	!	reproduce the original data.
	!	------------------------------------------------
	do mode = 1, nmodes
		!		----------------------------
		!		Get the normalization factor
		!		----------------------------
		sum = 0.0d0
		do i = 1, nx
			sum = sum + eigenvectors(i, mode) * eigenvectors(i, mode)
		end do
		fact = sqrt(sum)
		!		--------------------------
		!		Normalize the eigenvectors
		!		--------------------------
		if (fact.eq.0.0d0) then
			do i = 1, nx
				eigenvectors(i, mode) = 0.0d0
			end do
		else
			do i = 1, nx
				eigenvectors(i, mode) = eigenvectors(i, mode) / fact
			end do
		end if
		!		----------------------------------
		!		Normalize the principal components
		!		----------------------------------
		do i = 1, nt
			princomp(i, mode) = princomp(i, mode) * fact
		end do
	end do

	!	-------------------------------------------------
	!	Copy over just the requested number of
	!	eigenvalues, and calculate the cumulative percent
	!	variance explained.  Start by getting the total
	!	variance in the field, so we can normalize by
	!	that.
	!	-------------------------------------------------
	call deoftotvar(data, nx, nt, totvar, doswitched, &
			&icovcor, covariance, correlation, dmsg)
	if (DEBUG) then
		!print *, " "
		!print *, "totvar=", totvar
		!print *, " "
	end if

	sum = 0.0d0
	do jascending = nmodes, 1, -1
		jdescending = nmodes - jascending + 1
		eigenvalues(jdescending) = evals(jascending)
		variance(jdescending) = &
				&eigenvalues(jdescending) / totvar * 100.0d0
		sum = sum + variance(jdescending)
		cumvariance(jdescending) = sum
	end do

	return
end
! --------------------------------------------------------

subroutine deofcovcor(data, nx, nt, icovcor, covariance, &
		&correlation, spacked, doswitched, iminnxnt, dmsg)

	!	-------------------------------------------------
	!	Form the covariance or correlation matrix, put it
	!	into 's'.  Note that 's' is always symmetric --
	!	the correlation between X and Y is the same as
	!	between Y and X -- so use packed storage for 's'.
	!	The packed storage scheme we use is the same as
	!	LAPACK uses so we can pass 's' directly to the
	!	solver routine: the matrix is lower triangular,
	!	and s(i,j) = spacked(i+(j-1)*(1*n-j)/2).
	!
	!	Inputs:
	!		data(nx,nt): The basic data array.  THIS MUST
	!			BE ANOMALIES.
	!
	!		nx, nt: size of data array
	!			[INTEGER]
	!
	!		icovcor: if .eq. covariance, then calculate
	!			the covariance array;
	!			 if .eq. correlation, then calculate
	!			the correlation array.
	!			[INTEGER]
	!
	!		covariance, correlation: integer values to
	!			indicate each of these options.
	!			[INTEGER]
	!
	!		doswitched: if .TRUE., then calculate the
	!			'switched' array (which is of size
	!			(nt,nt)); if .FALSE., then calculate
	!			the normal array of size (nx,nx).
	!			[LOGICAL]
	!
	!		iminnxnt: min(nt,nx).  Used to dimension
	!			'spacked'.
	!
	!	Outputs:
	!
	!		spacked(iminnxnt*(iminnxnt+1)/2): the covariance
	!			or correlation array.  This is in packed
	!			form corresponding to LAPACK's lower
	!			triangular form.
	!
	!	David Pierce
	!	Scripps Institution of Oceanography
	!	Climate Research Division
	!	dpierce@ucsd.edu
	!	Jan 29, 1996
	!	-------------------------------------------------

	implicit none

	!	-----------------
	!	Passed parameters
	!	-----------------
	integer    nx, nt, icovcor, covariance, correlation, iminnxnt
	double precision data(nx, nt), spacked(iminnxnt * (iminnxnt + 1) / 2)
	double precision dmsg
	logical doswitched

	!	---------------
	!	Local variables
	!	---------------
	integer    i, j, k, npts
	double precision sum, sum2, sum3, fact

	if(nx .le. 1) then
		!print *, 'covariance: error: nx too small!! nx=', nx
		!call exit(-1)
		stop
	endif
	if(doswitched) then
		do j = 1, nt
			do i = j, nt
				sum = 0.0d0
				sum2 = 0.0d0
				sum3 = 0.0d0
				npts = 0
				do k = 1, nx
					if (data(k, i).ne.dmsg .and. &
							&data(k, j).ne.dmsg) then
						sum = sum + data(k, i) * data(k, j)
						sum2 = sum2 + data(k, i) * data(k, i)
						sum3 = sum3 + data(k, j) * data(k, j)
						npts = npts + 1
					end if
				enddo
				if(icovcor .eq. covariance) then
					!fact = 1.0d0/float(nx-1)
					fact = 1.0d0 / float(npts - 1)
				else
					fact = 1.0d0 / (sqrt(sum2) * sqrt(sum3))
				endif
				spacked(i + (j - 1) * (2 * nt - j) / 2) = sum * fact
			enddo
		enddo
	else
		do j = 1, nx
			do i = j, nx
				sum = 0.0d0
				sum2 = 0.0d0
				sum3 = 0.0d0
				npts = 0
				do k = 1, nt
					if (data(i, k).ne.dmsg .and. &
							&data(j, k).ne.dmsg) then
						sum = sum + data(j, k) * data(i, k)
						sum2 = sum2 + data(i, k) * data(i, k)
						sum3 = sum3 + data(j, k) * data(j, k)
						npts = npts + 1
					end if
				enddo
				if(icovcor .eq. covariance) then
					!fact = 1.0d0/float(nt-1)
					fact = 1.0d0 / float(npts - 1)
				else
					fact = 1.0d0 / (sqrt(sum2) * sqrt(sum3))
				endif
				spacked(i + (j - 1) * (2 * nx - j) / 2) = sum * fact
			enddo
		enddo
	endif

	return
end

! --------------------------------------------------------

subroutine deofpcs(data, nx, nt, nmodes, iminnxnt, &
		&imaxnxnt, evecs, doswitched, tentpcs, dmsg)

	!       ------------------------------------------------
	!       Compute the tentative principal components; they
	!       are 'tentative' because they might be the PCs
	!       of the switched data.  Put them into 'tentpcs',
	!       which is of size (nt,nmodes) if we are doing
	!       regular EOFs and (nx,nmodes) if we are doing
	!       switched EOFs.  These PCs come out in order
	!       corresponding to the order of 'evecs', which is
	!       in ASCENDING order.
	!
	!	Inputs:
	!
	!		data(nx,nt): The input data.  THESE MUST
	!			BE ANOMALIES.
	!
	!		nmodes: # of modes to calculate.
	!
	!		iminnxnt: min(nx,nt)
	!
	!		evecs(iminnxnt,nmodes): the eigenvectors
	!			(which might be switched).
	!
	!		doswitched: if .TRUE., then we are doing
	!			switched (space,time) calculation;
	!			otherwise, regular (time,space)
	!			calculation.
	!
	!	Outputs:
	!
	!		tentpcs(imaxnxnt,nmodes): the tentative
	!			(possibly switched) principal
	!			components.
	!
	!	David W. Pierce
	!	Scripps Institution of Oceanography
	!	Climate Research Division
	!	dpierce@ucsd.edu
	!	Jan 29, 1996
	!       ------------------------------------------------

	implicit none

	!	-----------------
	!	Passed parameters
	!	-----------------
	integer    nx, nt, nmodes, iminnxnt, imaxnxnt
	double precision data(nx, nt), evecs(iminnxnt, nmodes), &
			&tentpcs(imaxnxnt, nmodes), dmsg
	logical    doswitched

	!	---------------
	!	Local variables
	!	---------------
	integer    i, j, k
	double precision    sum

	if(doswitched) then
		do j = 1, nmodes
			do i = 1, nx
				sum = 0.0d0
				do k = 1, nt
					if (data(i, k).ne.dmsg) then
						sum = sum + data(i, k) * evecs(k, j)
					end if
				enddo
				tentpcs(i, j) = sum
			enddo
		enddo
	else
		do j = 1, nt
			do i = 1, nmodes
				sum = 0.0d0
				do k = 1, nx
					if (data(k, j).ne.dmsg) then
						sum = sum + data(k, j) * evecs(k, i)
					end if
				enddo
				tentpcs(j, i) = sum
			enddo
		enddo
	endif

	return
end

! ------------------------------------------

subroutine deoftotvar(data, nx, nt, totvar, doswitched, &
		&icovcor, covariance, correlation, dmsg)

	!	-------------------------------------------------
	!	Returns the total variance in the field so we can
	!	normalize by it.
	!
	!	Inputs:
	!
	!		data(nx,nt): data to calculate upon
	!
	!		nx, nt:	size of 'data'.
	!
	!		doswitched: if .TRUE., then we are working
	!			in switched (nx,nt) space, false
	!			otherwise.
	!
	!		icovcor: if (icovcor .eq. covariance), then
	!			we are using the covariance array;
	!			if( icovcor .eq. correlation) then
	!			we are using the correlation array.
	!
	!	Outputs:
	!
	!		totvar: estimate of total variance
	!
	!	-------------------------------------------------

	implicit none

	integer    nx, nt, icovcor, covariance, correlation
	double precision data(nx, nt), totvar, sum, fact, dmsg
	logical    doswitched
	integer    i, j, npts

	if(icovcor .eq. correlation) then
		if(doswitched) then
			totvar = nt
		else
			totvar = nx
		endif
		return
	endif

	totvar = 0.0d0
	if(doswitched) then
		fact = 1.0d0 / (nx - 1.0d0)
	else
		fact = 1.0d0 / (nt - 1.0d0)
	endif
	do j = 1, nt
		sum = 0.0d0
		npts = 0
		do i = 1, nx
			if (data(i, j).ne.dmsg) then
				sum = sum + data(i, j) * data(i, j)
				npts = npts + 1
			end if
		enddo
		fact = 1.0d0 / (npts - 1.0d0)
		totvar = totvar + sum * fact
	enddo

	return
end

