module m
contains

function sum_plain(a) result(res)
	implicit none
	real(8), intent(in) :: a(:)
	real(8) :: res
	integer(4) :: i
	res = 0
	do i = 1, size(a)
		res = res + a(i)
	end do
end function

function sum_omp(a) result(res)
	implicit none
	real(8), intent(in) :: a(:)
	real(8) :: res
	integer(4) :: i
	res = 0
	!$omp parallel do reduction(+:res)
	do i = 1, size(a)
		res = res + a(i)
	end do
end function

subroutine max_by_bin(a, bins, res)
	implicit none
	real(8),    intent(in) :: a(:)
	integer(4), intent(in) :: bins(:,:)
	real(8),    intent(inout) :: res(:)
	integer(4) :: i
	!$omp parallel do
	do i = 1, size(res)
		res(i) = maxval(a(bins(1,i)+1:bins(2,i)))
	end do
end subroutine

function mindist(vecs) result(res)
	implicit none
	real(8), intent(in) :: vecs(:,:)
	real(8) :: res
	integer(4) :: i, j, n
	n = size(vecs,2)
	res = sum((vecs(:,2)-vecs(:,1))**2)
	!$omp parallel do private(i,j) reduction(min:res) schedule(dynamic)
	do i = 1, n-1
		do j = i+1,n
			res = min(res, sum((vecs(:,i)-vecs(:,j))**2))
		end do
	end do
end function

end module
